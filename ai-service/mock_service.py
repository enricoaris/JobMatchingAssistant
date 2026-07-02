import time
import random
from typing import Dict, Any

class MockDocumentProcessor:
    def __init__(
        self,
        update_status_callback = None,
        client = None,
        update_queue = None,
        document_id: str = None,
        session_id: str = None, 
        document_type: str = None
    ):
        self.update_status = update_status_callback
        self.client = client
        self.update_queue = update_queue
        self.document_id = document_id
        self.session_id = session_id
        self.document_type = document_type

        from enums.document_status import JobStatus, ResumeStatus
        from enums.document_type import DocumentType
        self.StatusClass = JobStatus if document_type == DocumentType.JOB else ResumeStatus
    
    async def _update(self, status):
        from schemas.status_update import StatusUpdate

        await self.update_status(
            StatusUpdate(
                status=status,
                id=self.document_id,
                session_id=self.session_id
            ),
            client=self.client,
            update_queue=self.update_queue
        )
    
    async def _simulate_work(self, seconds: int):
        actual_delay = seconds + random.uniform(-0.5, 0.5)
        time.sleep(max(0.2, actual_delay))

    async def process_document(self, text: str = "") -> Dict[str, Any]:
        await self._update(self.StatusClass.GENERATING_EMBEDDING)
        await self._simulate_work(2)
        
        await self._update(self.StatusClass.EXTRACTING_SKILLS)
        await self._simulate_work(2)

        await self._update(self.StatusClass.EXTRACTING_REQUIREMENTS)
        await self._simulate_work(2)
        
        await self._update(self.StatusClass.EXTRACTING_HIGHLIGHTS)
        await self._simulate_work(2)

        mock_data = self._generate_mock_document_data()

        await self._update(self.StatusClass.COMPLETED)

        return mock_data

    async def process_insights(
            self,
            resume_text:str = "",
            job_text: str = ""
    ) -> Dict[str, Any]:
        await self._update(self.StatusClass.MATCHING)
        await self._simulate_work(3)
        
        # Generate insights
        insights = self._generate_mock_insights()
        
        # Status: Complete
        await self._update(self.StatusClass.MATCHING_COMPLETE)
        await self._simulate_work(1)

        return insights

    def _generate_mock_match_insights(self):
        match_levels = ["Strong", "Good", "Moderate", "Weak"]

        return {
            "assessment": {
                "match_level": random.choice(match_levels),
                "key_gaps": [
                    "Limited cloud deployment experience",
                    "No Kubernetes exposure"
                ],
                "assessment": (
                    "The candidate demonstrates strong backend "
                    "development skills with relevant API and "
                    "database experience. Technical alignment "
                    "with the job requirements is high."
                )
            },
            "suggestions": [
                "Learn Kubernetes fundamentals",
                "Build AWS deployment projects",
                "Improve CI/CD pipeline knowledge"
            ]
        }

    def _generate_mock_document_data(self):
        return {
            "embedding": [random.random() for _ in range(384)],
            "embedding_std": 0.52,
            "embedding_norm": 1.0,
            "skills": [
                "Python",
                "Docker",
                "PostgreSQL",
                "React"
            ],
            "skills_meta": {
                "Python": {
                    "Source": ["dict"],
                    "Confidence": 0.95
                },
                "Docker": {
                    "Source": ["llm"],
                    "Confidence": 0.87
                },
                "PostgreSQL": {
                    "Source": ["dict", "llm"],
                    "Confidence": 0.81
                }
            },
            "seniority": "Mid",
            "requirements": [
                "Experience with REST APIs",
                "Knowledge of SQL databases",
                "Understanding of CI/CD"
            ],
            "highlights": [
                "Built scalable backend APIs",
                "Worked with containerized deployment",
                "Collaborated in agile teams"
            ]
        }
