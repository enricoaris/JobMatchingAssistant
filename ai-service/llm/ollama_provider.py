import json
import re
from typing import Dict, List
from .interface import LLMProvider
from .prompts import (
    build_features_extraction_prompt,
    build_document_highlights_prompt,
    build_document_requirements_prompt,
    build_match_assessment_prompt,
    build_match_suggestions_prompt,
    build_skills_normalization_prompt
)

class OllamaProvider(LLMProvider):
    def __init__(self, host: str, model_name: str):
        try:
            import ollama
            self.client = ollama.Client(host=host)
        except ImportError:
            raise ImportError(
                "ollama package not installed. "
                "Install with: pip install ollama"
            )
        self.mode_name = model_name
        self._available = None
    
    def fetch_json_completion(self, system_prompt: str, user_prompt: str) -> str:
        try:
            response = self.client.chat(
                model=self.model_name,
                format="json",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ]
            )
            return response["message"]["content"]
        except Exception as e:
            raise RuntimeError(f"Ollama chat failed: {e}")
        
    def extract_features_with_llm(self, text: str) -> Dict:
        """Extract skills, experience, seniority from text"""
        system_prompt, user_prompt = build_features_extraction_prompt(text)
        content = self.fetch_json_completion(system_prompt, user_prompt)
        
        try:
            return json.loads(content)
        except json.JSONDecodeError as e:
            print(f"Failed to parse: {e}")
            return {"skills": [], "experience_years": None, "seniority": None}
    
    def generate_highlights(self, text: str) -> List[str]:
        """Extract highlights from resume"""
        system_prompt, user_prompt = build_document_highlights_prompt(text)
        content = self.fetch_json_completion(system_prompt, user_prompt)
        
        try:
            data = json.loads(content)
            return data.get("highlights", [])
        except json.JSONDecodeError as e:
            print(f"Failed to parse: {e}")
            return []
    
    def generate_requirements(self, text: str) -> List[str]:
        """Extract requirements from job description"""
        system_prompt, user_prompt = build_document_requirements_prompt(text)
        content = self.fetch_json_completion(system_prompt, user_prompt)
        
        try:
            data = json.loads(content)
            return data.get("requirements", [])
        except json.JSONDecodeError as e:
            print(f"Failed to parse: {e}")
            return []
    
    def generate_assessments(self, match_input: Dict) -> Dict:
        """Generate match assessment"""
        system_prompt, user_prompt = build_match_assessment_prompt(match_input)
        content = self.fetch_json_completion(system_prompt, user_prompt)
        
        try:
            data = json.loads(content)
            return {
                "match_level": data.get("match_level", "unknown"),
                "assessment": data.get("assessment", ""),
                "key_gaps": data.get("key_gaps", [])
            }
        except json.JSONDecodeError as e:
            print(f"Failed to parse: {e}")
            return {"match_level": "unknown", "assessment": "", "key_gaps": []}
    
    def generate_suggestions(self, match_input: Dict) -> List[str]:
        """Generate career suggestions"""
        system_prompt, user_prompt = build_match_suggestions_prompt(match_input)
        content = self.fetch_json_completion(system_prompt, user_prompt)
        
        try:
            data = json.loads(content)
            return data.get("actions", [])
        except json.JSONDecodeError as e:
            print(f"Failed to parse: {e}")
            return []
    
    def normalize_skills_with_llm(self, skill_list: List[str]) -> List[str]:
        system_prompt, user_prompt = build_skills_normalization_prompt(skill_list)
        content = self.fetch_json_completion(system_prompt, user_prompt)
        
        try:
            data = json.loads(content)
            return data.get("normalized_skills", [])
        except json.JSONDecodeError as e:
            print(f"Failed to parse: {e}")
            return skill_list  # Return original if parsing fails
    
    def is_available(self) -> bool:
        if self._available is not None:
            return self._available
        
        try:
            self.client.list()
            self._available = True
        except:
            self._available = False
        
        return self._available