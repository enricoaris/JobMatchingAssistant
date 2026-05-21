from enum import StrEnum
from settings import API_URL

class QueueName(StrEnum):
    RESUME_EXTRACTED = "resume-text-extracted"
    JOB_UPLOADED = "job-description-uploaded"
    JOB_STATUS_UPDATED = "job-status-updated"
    RESUME_STATUS_UPDATED = "resume-status-updated"
    MATCHING_COMPLETED = "matching-completed"

class ApiService(StrEnum):
    JOB_EMBEDDING = API_URL + "/job/embedding"
    RESUME_EMBEDDING = API_URL + "/resume/embedding"
    MATCH_INSIGHTS = API_URL + "/match/insights"