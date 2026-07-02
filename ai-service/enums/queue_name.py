from enum import StrEnum

class QueueName(StrEnum):
    RESUME_EXTRACTED = "resume-text-extracted"
    JOB_UPLOADED = "job-description-uploaded"
    JOB_STATUS_UPDATED = "job-status-updated"
    RESUME_STATUS_UPDATED = "resume-status-updated"
    MATCHING_COMPLETED = "matching-completed"