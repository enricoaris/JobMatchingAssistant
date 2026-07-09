import json
import time
import random
from typing import Dict, List, Any
from .interface import LLMProvider

class MockProvider(LLMProvider):
    def __init__(self, delay: float = 1.0):
        self.delay = delay
    
    def fetch_json_completion(self, system_prompt: str, user_prompt: str) -> str:
        """Simulate LLM response based on prompt content"""
        time.sleep(self.delay)
        
        # Return different mock responses based on what's being asked
        if "extract structured data" in system_prompt or "extract features" in system_prompt:
            return self._mock_features_response()
        
        elif "candidate highlights" in system_prompt or "highlights from a resume" in system_prompt:
            return self._mock_highlights_response()
        
        elif "job requirements" in system_prompt or "extract structured requirements" in system_prompt:
            return self._mock_requirements_response()
        
        elif "match assessment" in system_prompt or "job matching analyst" in system_prompt:
            return self._mock_assessment_response()
        
        elif "career advisor" in system_prompt or "improvement strings" in system_prompt:
            return self._mock_suggestions_response()
        
        elif "normalize" in system_prompt or "data normalization engine" in system_prompt:
            return self._mock_normalize_response()
        
        else:
            return self._mock_generic_response()
    
    def extract_features_with_llm(self, text: str) -> Dict:
        """Mock skills, experience, seniority extraction"""
        return {
            "skills": ["Python", "Docker", "PostgreSQL", "React", "AWS"],
            "experience_years": 5.0,
            "seniority": "senior",
            "confidence": 0.92
        }
    
    def generate_highlights(self, text: str) -> List[str]:
        """Mock highlights extraction"""
        return [
            "Built scalable microservices with Python and Docker",
            "Led a team of 5 engineers on a major project",
            "Reduced API response time by 40% through optimization"
        ]
    
    def generate_requirements(self, text: str) -> List[str]:
        """Mock requirements extraction"""
        return [
            "5+ years of software development experience",
            "Experience with Python and cloud platforms",
            "Strong understanding of REST APIs and microservices",
            "Knowledge of CI/CD pipelines",
            "Experience with PostgreSQL or similar databases"
        ]
    
    def generate_assessments(self, match_input: Dict) -> Dict:
        """Mock match assessment"""
        levels = ["strong", "moderate", "weak"]
        return {
            "match_level": random.choice(levels),
            "assessment": "Candidate shows strong alignment with key technical requirements",
            "key_gaps": [
                "Limited cloud deployment experience",
                "No Kubernetes exposure"
            ]
        }
    
    def generate_suggestions(self, match_input: Dict) -> List[str]:
        """Mock career suggestions"""
        return [
            "Learn Kubernetes fundamentals",
            "Build AWS deployment projects",
            "Improve CI/CD pipeline knowledge",
            "Contribute to open-source projects"
        ]
    
    def normalize_skills_with_llm(self, skill_list: List[str]) -> List[str]:
        """Mock skill normalization"""
        # Just clean them up without LLM
        normalized = []
        for skill in skill_list:
            cleaned = skill.lower().strip()
            if cleaned:
                normalized.append(cleaned)
        return list(set(normalized))
    
    def is_available(self) -> bool:
        """Mock is always available"""
        return True
    
    # Private methods for JSON responses
    
    def _mock_features_response(self) -> str:
        return json.dumps({
            "skills": ["python", "docker", "postgresql", "react", "aws"],
            "experience_years": 5.0,
            "seniority": "senior",
            "confidence": 0.92
        })
    
    def _mock_highlights_response(self) -> str:
        return json.dumps({
            "highlights": [
                "Built scalable microservices with Python and Docker",
                "Led a team of 5 engineers on a major project",
                "Reduced API response time by 40%"
            ]
        })
    
    def _mock_requirements_response(self) -> str:
        return json.dumps({
            "requirements": [
                "5+ years of software development experience",
                "Experience with Python and cloud platforms",
                "Strong understanding of REST APIs",
                "Knowledge of CI/CD pipelines"
            ]
        })
    
    def _mock_assessment_response(self) -> str:
        levels = ["strong", "moderate", "weak"]
        return json.dumps({
            "match_level": random.choice(levels),
            "assessment": "Candidate shows strong alignment with key technical requirements",
            "key_gaps": ["Limited cloud deployment experience"]
        })
    
    def _mock_suggestions_response(self) -> str:
        return json.dumps({
            "actions": [
                "Learn Kubernetes fundamentals",
                "Build AWS deployment projects",
                "Improve CI/CD pipeline knowledge"
            ]
        })
    
    def _mock_normalize_response(self) -> str:
        return json.dumps({
            "normalized_skills": ["python", "javascript", "react", "node.js"]
        })
    
    def _mock_generic_response(self) -> str:
        return json.dumps({
            "result": "Mock response generated successfully"
        })