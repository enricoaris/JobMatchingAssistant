# enums/document_status.py
from enum import IntEnum
from typing import Dict, Optional

class JobStatus(IntEnum):
    """Statuses for job description processing"""
    
    # Initial states
    UPLOADED = 0
    QUEUED = 1
    
    # Processing states
    GENERATING_EMBEDDING = 10
    EXTRACTING_SKILLS = 11
    EXTRACTING_REQUIREMENTS = 12
    EXTRACTING_HIGHLIGHTS = 13
    
    # Terminal states
    COMPLETED = 20
    FAILED = 30
    
    # Mock states
    MOCK_PROCESSING = 40
    MOCK_COMPLETED = 41

    @property
    def display_name(self) -> str:
        return {
            JobStatus.UPLOADED: "Uploaded",
            JobStatus.QUEUED: "Queued",
            JobStatus.GENERATING_EMBEDDING: "Generating Embedding",
            JobStatus.EXTRACTING_SKILLS: "Extracting Skills",
            JobStatus.EXTRACTING_REQUIREMENTS: "Extracting Requirements",
            JobStatus.EXTRACTING_HIGHLIGHTS: "Extracting Highlights",
            JobStatus.COMPLETED: "Completed",
            JobStatus.FAILED: "Failed",
            JobStatus.MOCK_PROCESSING: "Generating Mock Data",
            JobStatus.MOCK_COMPLETED: "Mock Complete",
        }.get(self, str(self))
    
    @property
    def progress(self) -> int:
        return {
            JobStatus.UPLOADED: 0,
            JobStatus.QUEUED: 5,
            JobStatus.GENERATING_EMBEDDING: 25,
            JobStatus.EXTRACTING_SKILLS: 50,
            JobStatus.EXTRACTING_REQUIREMENTS: 75,
            JobStatus.EXTRACTING_HIGHLIGHTS: 90,
            JobStatus.COMPLETED: 100,
            JobStatus.FAILED: 0,
            JobStatus.MOCK_PROCESSING: 50,
            JobStatus.MOCK_COMPLETED: 100,
        }.get(self, 0)
    
    @property
    def is_terminal(self) -> bool:
        return self in [JobStatus.COMPLETED, JobStatus.FAILED, JobStatus.MOCK_COMPLETED]

class ResumeStatus(IntEnum):
    """Statuses for resume processing"""
    
    # Initial states
    UPLOADED = 0
    QUEUED = 1
    
    # Processing states
    TEXT_EXTRACTED = 10,

    GENERATING_EMBEDDING = 20,
    EXTRACTING_SKILLS = 21,
    EXTRACTING_REQUIREMENTS = 22,
    EXTRACTING_HIGHLIGHTS = 23,
    
    # Matching states (if you do matching in this service)
    MATCHING = 30
    MATCHING_COMPLETE = 31
    
    # Terminal states
    COMPLETED = 40
    FAILED = 50
    
    # Mock states
    MOCK_PROCESSING = 60
    MOCK_COMPLETED = 61

    @property
    def display_name(self) -> str:
        return {
            ResumeStatus.UPLOADED: "Uploaded",
            ResumeStatus.QUEUED: "Queued",
            ResumeStatus.GENERATING_EMBEDDING: "Generating Embedding",
            ResumeStatus.EXTRACTING_SKILLS: "Extracting Skills",
            ResumeStatus.MATCHING: "Matching Against Jobs",
            ResumeStatus.MATCHING_COMPLETE: "Matching Complete",
            ResumeStatus.COMPLETED: "Completed",
            ResumeStatus.FAILED: "Failed",
            ResumeStatus.MOCK_PROCESSING: "Generating Mock Data",
            ResumeStatus.MOCK_COMPLETED: "Mock Complete",
        }.get(self, str(self))
    
    @property
    def progress(self) -> int:
        return {
            ResumeStatus.UPLOADED: 0,
            ResumeStatus.QUEUED: 5,
            ResumeStatus.GENERATING_EMBEDDING: 40,
            ResumeStatus.EXTRACTING_SKILLS: 60,
            ResumeStatus.MATCHING: 80,
            ResumeStatus.MATCHING_COMPLETE: 95,
            ResumeStatus.COMPLETED: 100,
            ResumeStatus.FAILED: 0,
            ResumeStatus.MOCK_PROCESSING: 50,
            ResumeStatus.MOCK_COMPLETED: 100,
        }.get(self, 0)
    
    @property
    def is_terminal(self) -> bool:
        return self in [ResumeStatus.COMPLETED, ResumeStatus.FAILED, ResumeStatus.MOCK_COMPLETED]