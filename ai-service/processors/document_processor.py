import requests
import json
from enums.queue_name import QueueName
from enums.api_service import ApiService
from skill_mapping import SKILLS
from messaging.rabbit_client import RabbitClient
from llm_service import (
    generate_embedding, normalize_text, extract_features_with_llm,
    extract_skills_with_dict, basic_cleanup_skill, generate_highlights,
    generate_requirements, generate_assessments, generate_suggestions
)
from settings import USE_MOCK_LLM
from mock_service import MockDocumentProcessor
import logging
import time
from factories.status_factory import StatusFactory
from enums.document_status import JobStatus, ResumeStatus
from enums.document_type import DocumentType
from schemas.status_update import StatusUpdate

logging.basicConfig(
    level=logging.INFO,
    format=(
        "%(asctime)s %(levelname)s "
        "[doc=%(document_id)s session=%(session_id)s queue=%(queue_name)s] "
        "%(message)s"
        )
)

logger = logging.getLogger(__name__)

async def update_status(
    status_update: StatusUpdate,
    client: RabbitClient,
    update_queue: str
):
    if logger:
        logger.info(
            f"Updating Status: {status_update.status.display_name}",
            extra=status_update.to_log_extra()
        )
    
    await client.publish(
        queue_name=update_queue,
        body=status_update.to_message()
    )

def merge_skills(dict_skills, llm_skills):
    merged = {}

    for skill in dict_skills:
        merged[skill] = {
            "source": ["dict"],
            "confidence": 0.7
        }
    
    for skill in llm_skills:
        if skill in merged:
            merged[skill]["source"].append("llm")
            merged[skill]["confidence"] = 1.0
        else:
            merged[skill] = {
                "source": ["llm"],
                "confidence": 0.8
            }
    
    return merged

def parse_message_data(message_body: bytes):
    try:
        data = json.loads(message_body)
        
        return {
            "id": data.get("Id"),
            "text": data.get("Text"),
            "session_id": data.get("SessionId")
        }
    except json.JSONDecodeError:
        print("Error: Received invalid JSON.")
        return None

async def process_document(
    message:any,
    client: RabbitClient,
    target_api: ApiService,
    update_queue: QueueName,
    document_type: DocumentType
):
    extracted = parse_message_data(message.body)
    if not extracted:
        return type('Response', (object,), {"status_code": 400})
    
    StatusClass = StatusFactory.get_status_class(document_type.value)
    document_id = extracted["id"]
    session_id = extracted["session_id"]

    log_extra = {
        "queue_name": update_queue,
        "document_id": document_id,
        "session_id": session_id,
        "document_type": document_type.value
    }

    try:
        if USE_MOCK_LLM:
            mock_processor = MockDocumentProcessor(
                update_status_callback=update_status,
                client=client,
                update_queue=update_queue,
                document_id=document_id,
                session_id=session_id,
                document_type=document_type
            )

            mock_data = await mock_processor.process_document(text=extracted["text"])

            payload = {
                "Id": document_id,
                "DocumentType": document_type,
                "SessionId": session_id,
                **mock_data  # Unpack mock data
            }

            response = requests.post(target_api, json=payload, verify=False)
            return response

        await update_status(
            StatusUpdate(
                status=StatusClass.GENERATING_EMBEDDING,
                id=document_id,
                session_id=extracted["session_id"],
            ),
            client=client,
            update_queue=update_queue
        )

        logger.info("Generating Embedding.",extra=log_extra)

        embedding, embedding_std, embedding_norm = generate_embedding(extracted["text"])
        normalized_text = normalize_text(extracted["text"])

        time.sleep(0.5)
        await update_status(
            StatusUpdate(
                status=StatusClass.EXTRACTING_SKILLS,
                id=document_id,
                session_id=extracted["session_id"],
            ),
            client=client,
            update_queue=update_queue
        )
        logger.info("Extracting Skills.", extra=log_extra)
        
        dict_skills = extract_skills_with_dict(normalized_text, skills_dict=SKILLS)
        llm_features = extract_features_with_llm(normalized_text)

        merged_skills = merge_skills(dict_skills, llm_features["skills"])
        normalized_skills = []
        for skill in list(merged_skills.keys()):
            normalized_skills.append(basic_cleanup_skill(skill))

        await update_status(
            StatusUpdate(
                status=StatusClass.EXTRACTING_REQUIREMENTS,
                id=document_id,
                session_id=extracted["session_id"],
            ),
            client=client,
            update_queue=update_queue
        )
        requirements = generate_requirements(normalized_text)
        
        await update_status(
            StatusUpdate(
                status=StatusClass.EXTRACTING_HIGHLIGHTS,
                id=document_id,
                session_id=extracted["session_id"],
            ),
            client=client,
            update_queue=update_queue
        )
        highlights = generate_highlights(normalized_text)

        payload = {
            "Id": document_id,
            "DocumentType": document_type,
            "Embedding": embedding.tolist(),
            "EmbeddingStd": embedding_std,
            "EmbeddingNorm": embedding_norm,
            "Skills": normalized_skills,
            "SkillsMeta": merged_skills,
            "SessionId": extracted["session_id"],
            "Requirements": requirements,
            "Highlights": highlights,
            "Seniority": llm_features.get("seniority"),
        }

        logger.info("Sending processed document", extra=log_extra)
        response = requests.post(target_api, json=payload, verify=False)
        
        if (response.status_code == 200):
            await update_status(
                StatusUpdate(
                    status=StatusClass.COMPLETED,
                    id=document_id,
                    session_id=extracted["session_id"],
                ),
                client=client,
                update_queue=update_queue
            )
        else:
            await update_status(
                StatusUpdate(
                    status=StatusClass.FAILED,
                    id=document_id,
                    session_id=extracted["session_id"],
                    additional_data={
                        "Error": f"API returned{response.status_code}",
                        "ErrorDetail": response.text[:200]
                    }
                ),
                client=client,
                update_queue=update_queue,
            )

        logger.info(
            "API responded",
            extra={
                **log_extra,
                "status_code": response.status_code
            }
        )

        return response
    
    except Exception as e:
        logger.exception(
            "Document Processing failed.",
            extra=log_extra
        )

        await update_status(
            StatusUpdate(
                status=StatusClass.FAILED,
                id=document_id,
                session_id=extracted["session_id"],
                additional_data={
                    "Error": str(e),
                    "ErrorType": type(e).__name__
                }
            ),
            client=client,
            update_queue=update_queue,
        )

        raise

async def process_resume(message:any, client: RabbitClient):
    return await process_document(
        message,
        client,
        target_api=ApiService.RESUME_EMBEDDING,
        update_queue=QueueName.RESUME_STATUS_UPDATED,
        document_type=DocumentType.RESUME
    )

async def process_job(message:any, client:RabbitClient):
    return await process_document(
        message,
        client,
        target_api=ApiService.JOB_EMBEDDING,
        update_queue=QueueName.JOB_STATUS_UPDATED,
        document_type=DocumentType.JOB
    )

async def process_insights(message:any, client: RabbitClient):
    try :
        data = json.loads(message.body)
        match_id = data.get("MatchId")
        resume_id = data.get("ResumeId")
        session_id = data.get("SessionId")

        match_input = {
            "job": {
                "requirements": data.get("jobRequirements"),
                "highlights": data.get("jobHighlights")
            },
            "resume": {
                "skills": data.get("resumeSkills"),
                "highlights": data.get("resumeHighlights")
            }
        }

        if USE_MOCK_LLM:
            mock_processor = MockDocumentProcessor(update_status_callback=update_status)
            mock_insights = mock_processor._generate_mock_match_insights()

            assessments = mock_insights["assessment"]
            suggestions = mock_insights["suggestions"]
        else:
            assessments = generate_assessments(match_input)
            suggestions = generate_suggestions(match_input)

        payload = {
            "MatchId": match_id,
            "Suggestions": suggestions,
            "MatchLevel": assessments["match_level"],
            "KeyGaps": assessments["key_gaps"],
            "Assessment": assessments["assessment"]
        }

        response = requests.post(
            ApiService.MATCH_INSIGHTS,
            json=payload,
            verify=False
        )

        if response.status_code == 200:
            await update_status(
                StatusUpdate(
                    status=ResumeStatus.COMPLETED,
                    id=resume_id,
                    session_id=session_id,
                    additional_data={
                        "Error": f"API returned{response.status_code}",
                        "ErrorDetail": response.text[:200]
                    }
                ),
                client=client,
                update_queue=QueueName.RESUME_STATUS_UPDATED,
            )

        return response
    except json.JSONDecodeError:
        print("Error: Received invalid JSON.")
        return None