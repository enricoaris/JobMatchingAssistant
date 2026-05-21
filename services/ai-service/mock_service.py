import time
import random

def generate_mock_match_insights(text: str):
    time.sleep(2)

    return {
        "assessment": {
            "match_level": "Strong",
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

def generate_mock_document_data(text: str):
    time.sleep(2)

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
