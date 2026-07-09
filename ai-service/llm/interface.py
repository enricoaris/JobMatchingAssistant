from abc import ABC, abstractmethod
from typing import Dict, List

class LLMProvider(ABC):
    @abstractmethod
    def fetch_json_completion(self, system_prompt: str, user_prompt: str) -> str:
        """Fetch JSON completion from LLM"""
        pass
    
    @abstractmethod
    def extract_features_with_llm(self, text: str) -> Dict:
        """Extract skills, experience, seniority from text"""
        pass
    
    @abstractmethod
    def generate_highlights(self, text: str) -> List[str]:
        """Extract highlights from resume"""
        pass
    
    @abstractmethod
    def generate_requirements(self, text: str) -> List[str]:
        """Extract requirements from job description"""
        pass
    
    @abstractmethod
    def generate_assessments(self, match_input: Dict) -> Dict:
        """Generate match assessment"""
        pass
    
    @abstractmethod
    def generate_suggestions(self, match_input: Dict) -> List[str]:
        """Generate career suggestions"""
        pass
    
    @abstractmethod
    def normalize_skills_with_llm(self, skill_list: List[str]) -> List[str]:
        """Normalize skills using LLM"""
        pass
    
    @abstractmethod
    def is_available(self) -> bool:
        """Check if LLM is available"""
        pass

