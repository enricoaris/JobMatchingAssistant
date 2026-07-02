from settings import API_URL
from enum import StrEnum

class ApiService(StrEnum):
    JOB_EMBEDDING = API_URL + "/job/embedding"
    RESUME_EMBEDDING = API_URL + "/resume/embedding"
    MATCH_INSIGHTS = API_URL + "/match/insights"