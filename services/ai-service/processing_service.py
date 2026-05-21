import requests
import json
from enums import QueueName, ApiService
from skill_mapping import SKILLS
from messaging.rabbit_client import RabbitClient
from llm_service import (
    generate_embedding, normalize_text, extract_features_with_llm,
    extract_skills_with_dict, basic_cleanup_skill, generate_highlights,
    generate_requirements, generate_assessments, generate_suggestions
)
from settings import USE_MOCK_LLM
from mock_service import generate_mock_document_data, generate_mock_match_insights

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

async def process_document(message:any, client: RabbitClient, target_api: ApiService, update_queue: QueueName):
    async def update_status(status_text: str, queue_name: QueueName):
        await client.publish(
            queue_name=queue_name,
            body={
                "Id": extracted["id"],
                "Status": status_text,
                "SessionId": extracted["session_id"],
            }
        )
    
    extracted = parse_message_data(message.body)
    if not extracted:
        return type('Response', (object,), {"status_code": 400})

    if USE_MOCK_LLM:
        await update_status("Generating Mock AI Data.", update_queue)

        mock_data = generate_mock_document_data(extracted["text"])

        payload = {
            "Id": extracted["id"],
            "Embedding": mock_data["embedding"],
            "EmbeddingStd": mock_data["embedding_std"],
            "EmbeddingNorm": mock_data["embedding_norm"],
            "Skills": mock_data["skills"],
            "SkillsMeta": mock_data["skills_meta"],
            "Seniority": mock_data["seniority"],
            "SessionId": extracted["session_id"],
            "Requirements": mock_data["requirements"],
            "Highlights": mock_data["highlights"]
        }

        response = requests.post(target_api, json=payload, verify=False)

        if response.status_code == 200:
            await update_status("Mock Process Completed.", update_queue)

        return response

    await update_status( "Generating Embedding.", update_queue)

    embedding, embedding_std, embedding_norm = generate_embedding(extracted["text"])

    await update_status( "Extracting Skills.", update_queue)

    normalized_text = normalize_text(extracted["text"])
    dict_skills = extract_skills_with_dict(normalized_text, skills_dict=SKILLS)
    llm_features = extract_features_with_llm(normalized_text)

    merged_skills = merge_skills(dict_skills, llm_features["skills"])
    normalized_skills = []

    for skill in list(merged_skills.keys()):
        normalized_skills.append(basic_cleanup_skill(skill))

    await update_status( "Extracting Requirements.", update_queue)

    requirements = generate_requirements(normalized_text)

    await update_status( "Extracting Highlights.", update_queue)

    highlights = generate_highlights(normalized_text)

    payload = {
        "Id": extracted["id"],
        "Embedding": embedding.tolist(),
        "EmbeddingStd": embedding_std,
        "EmbeddingNorm": embedding_norm,
        "Skills": normalized_skills,
        "SkillsMeta": merged_skills,
        "Seniority": llm_features["seniority"],
        # "ExperienceYears": llm_features["experience_years"],
        "SessionId": extracted["session_id"],
        "Requirements": requirements,
        "Highlights": highlights
    }

    response = requests.post(target_api, json=payload, verify=False)

    if (response.status_code == 200):
        await update_status("Process Completed.", update_queue)

    return response

async def process_resume(message:any, client: RabbitClient):
    return await process_document(
        message, client, target_api=ApiService.RESUME_EMBEDDING, update_queue=QueueName.RESUME_STATUS_UPDATED
    )

async def process_job(message:any, client:RabbitClient):
    return await process_document(
        message, client, target_api=ApiService.JOB_EMBEDDING, update_queue=QueueName.JOB_STATUS_UPDATED
    )

async def process_insights(message:any, client: RabbitClient):
    try :
        data = json.loads(message.body)
        match_id = data.get("MatchId")

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
            mock_insights = generate_mock_match_insights()

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

        return response
    except json.JSONDecodeError:
        print("Error: Received invalid JSON.")
        return None