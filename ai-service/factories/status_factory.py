from typing import Union
from enums.document_status import JobStatus, ResumeStatus
from enums.document_type import DocumentType

class StatusFactory:
    @staticmethod
    def get_status_class(document_type: DocumentType) -> Union[JobStatus, ResumeStatus]:
        if document_type == DocumentType.JOB:
            return JobStatus
        elif document_type == DocumentType.RESUME:
            return ResumeStatus
        else:
            raise ValueError(f"Unknown document type: {document_type}")
        
    @staticmethod
    def get_default_status(document_type: str):
        status_class = StatusFactory.get_status_class(document_type)
        return status_class.UPLOADED

    @staticmethod
    def get_next_status(document_type: str, current_status_name: str):
        job_sequence = [
            JobStatus.UPLOADED,
            JobStatus.QUEUED,
            JobStatus.GENERATING_EMBEDDING,
            JobStatus.EXTRACTING_SKILLS,
            JobStatus.EXTRACTING_REQUIREMENTS,
            JobStatus.EXTRACTING_HIGHLIGHTS,
            JobStatus.COMPLETED,
        ]

        resume_sequence = [
            ResumeStatus.UPLOADED,
            ResumeStatus.QUEUED,
            ResumeStatus.GENERATING_EMBEDDING,
            ResumeStatus.COMPLETED,
        ]

        if document_type == "job":
            for i, status in enumerate(job_sequence):
                if status.name == current_status_name and i < len(job_sequence) - 1:
                    return job_sequence[i + 1]
        else:
             for i, status in enumerate(resume_sequence):
                 if status.name == current_status_name and i < len(resume_sequence) - 1:
                     return resume_sequence[i + 1]
        return None