import re
import os
import numpy as np
from sentence_transformers import SentenceTransformer

DEFAULT_MODEL = os.getenv("EMBEDDING_MODEL", "all-MiniLM-L6-v2")
model = SentenceTransformer(DEFAULT_MODEL)

def normalize_text(text):
    text = text.lower()
    text = re.sub(r'[^a-z0-9+#.\s]', ' ', text)
    return text

def basic_cleanup_skill(skill: str):
    skill = skill.lower()
    skill = re.sub(r"\(.*?\)", "", skill)  # remove brackets
    skill = re.sub(r"[^a-z0-9+#.\s]", " ", skill)
    skill = re.sub(r"\s+", " ", skill).strip()
    return skill

def generate_embedding(text):
    embedding = np.array(model.encode(text, normalize_embeddings=True).tolist())
    embedding_std = np.std(embedding)
    embedding_norm = np.linalg.norm(embedding)

    return (embedding, embedding_std, embedding_norm)

# def fetch_json_completion(system_prompt, user_prompt):
#     response = CLIENT.chat(
#         model=OLLAMA_MODEL_NAME,
#         format="json",
#         messages=[
#             {"role": "system", "content": system_prompt},
#             {"role": "user", "content": user_prompt}
#         ]
#     )

#     content = response["message"]["content"]

#     return content

def extract_skills_with_dict(text, skills_dict):
    text = normalize_text(text)
    found = set()

    for canonical, aliases in skills_dict.items():
        for alias in aliases:
            # create safe regex pattern
            pattern = r'\b' + re.escape(alias.lower()) + r'\b'
            if re.search(pattern, text):
                found.add(canonical)
                break  

    return list(found)



# def extract_features_with_llm(text):
#     system_prompt, user_prompt = build_features_extraction_prompt(text)

#     content = fetch_json_completion(system_prompt, user_prompt)

#     try:
#         return json.loads(content)
#     except json.JSONDecodeError as e:
#         print(f"Failed to parse: {e}")
#         return ""
    
# def normalize_skills_with_llm(skill_list):
#     system_prompt, user_prompt = build_skills_normalization_prompt(skill_list)

#     content = fetch_json_completion(system_prompt, user_prompt)

#     try:
#         return json.loads(content)
#     except json.JSONDecodeError as e:
#         print(f"Failed to parse {e}")
#         return ""
    
# def generate_highlights(text):
#     system_prompt, user_prompt = build_document_highlights_prompt(text)

#     content = fetch_json_completion(system_prompt, user_prompt)

#     try:
#         data = json.loads(content)

#         if not isinstance(data, dict):
#             return []

#         highlights = data.get("highlights")

#         if not isinstance(highlights, list):
#             return []
        
#         return highlights
#     except json.JSONDecodeError as e:
#         print(f"Failed to parse {e}")
#         return ""

# def generate_requirements(text):
#     system_prompt, user_prompt = build_document_requirements_prompt(text)

#     content = fetch_json_completion(system_prompt, user_prompt)

#     try:
#         data = json.loads(content)

#         if not isinstance(data, dict):
#             return []

#         requirements = data.get("requirements")

#         if not isinstance(requirements, list):
#             return []
        
#         return requirements
#     except json.JSONDecodeError as e:
#         print(f"Failed to parse {e}")
#         return ""

# def generate_assessments(match_input: dict):
#     system_prompt, user_prompt = build_match_asssesment_prompt(match_input)

#     content = fetch_json_completion(system_prompt, user_prompt)

#     try:
#         data = json.loads(content)

#         match_level = data.get("match_level")
#         assessment = data.get("assessment")
#         key_gaps = data.get("key_gaps", [])
        
#         return {
#             "match_level": match_level,
#             "assessment": assessment,
#             "key_gaps": key_gaps
#         }
#     except json.JSONDecodeError as e:
#         print(f"Failed to parse {e}")
#         return ""

# def generate_suggestions(match_input: dict):
#     system_prompt, user_prompt = build_match_suggestions_prompt(match_input)
    
#     content = fetch_json_completion(system_prompt, user_prompt)

#     try:
#         data = json.loads(content)
#         actions = data.get("actions")

#         return actions
#     except json.JSONDecodeError as e:
#         print(f"Failed to parse {e}")
        # return ""