def build_features_extraction_prompt(text):
    system_prompt = f"""
            You are an information extraction system.

            Extract structured data from user-provided text.

            Return ONLY valid JSON. No explanation.

            Rules:
            - Extract technical skills only (programming, frameworks, tools, cloud)
            - Normalize skill names (e.g., "js" to "javascript", "nodejs" to "node.js")
            - Remove duplicates

            Output format:
            {{
                "skills": ["string"],          // Normalized list: e.g., ["javascript", "react", "postgresql"]
                "experience_years": number,     // Total years as a float or null
                "seniority": "string",         // Strictly one of: "junior", "mid", "senior", or null
                "confidence": number           // Float between 0.0 and 1.0
            }}
        """

    user_prompt = f"""
        Text:
        \"\"\"{text}\"\"\"
    """
    
    return system_prompt, user_prompt

def build_document_highlights_prompt(document_text):
    system_prompt = """
        You are an information extraction engine.

        Your task is to extract key candidate highlights from a resume.

        Rules:
        - Return ONLY valid JSON
        - Do NOT include explanations
        - Keep each highlight concise (max 15 words)
        - Focus on skills, tools, and achievements
        - Avoid generic phrases (e.g., "hardworking", "team player")

        Schema:
        {
            "highlights": string[]
        }
    """

    user_prompt = f"""
        Resume:
        \"\"\"{document_text}\"\"\"
    """

    return system_prompt, user_prompt

def build_document_requirements_prompt(document_text):
    system_prompt = """
        You are an information extraction engine.

        Your task is to extract structured job requirements.

        Rules:
        - Return ONLY valid JSON
        - Do NOT include explanations
        - Normalize skills to lowercase
        - Keep skills short and standard
        - Do NOT include duplicates

        Schema:
        {
            "requirements": string[]
        }
    """
    user_prompt = f"""
        Extract structured requirements from the following description.

        Input:
        {document_text}
    """

    return system_prompt, user_prompt

def build_skills_normalization_prompt(skill_list):
    system_prompt = """
        You are a data normalization engine.

        Rules:
        - Return ONLY valid JSON
        - Do NOT include explanations
        - Follow the exact schema strictly

        Schema:
        {
        "normalized_skills": string[]
        }

        Normalization guidelines:
        - Convert all skills to lowercase
        - Remove unnecessary words or context
        - Split complex phrases into atomic skills
        - Keep only widely recognized technical skills
        - Do NOT invent new skills
        - Do NOT include duplicates
    """

    user_prompt = f"""
        Normalize the following skills:

        Input:
        {skill_list}
    """

    return system_prompt, user_prompt

def build_match_assessment_prompt(match_input: dict):
    system_prompt = """
        You are a job matching analyst.

        Your task is to evaluate how well a candidate matches a job based on structured matching data.

        Rules:
        - Return ONLY valid JSON
        - Do NOT include explanations outside JSON
        - Be objective and concise
        - Do NOT restate the input
        - Focus on fit evaluation and key skill gaps
    """
    user_prompt = f"""
        Input:
        {match_input}

         Task:
        1. Compare job requirements with candidate skills and highlights
        2. Identify strong alignments between the candidate and the role
        3. Identify important missing or weak areas
        4. Evaluate the overall candidate fit

        Return JSON:
        {{
            "match_level": "strong | moderate | weak",
            "assessment": "Max 15 words",
            "key_gaps": [
                "Max 3 missing or weak areas"
            ]
        }}

         Guidelines:
        - Infer gaps yourself from the provided data
        - Consider both explicit skills and implied experience from highlights
        - Keep the assessment short, clear, and human-readable
        - Avoid generic statements
        - key_gaps should contain only meaningful missing areas

        Match Level Criteria:
        - strong:
          Most important requirements are covered with clear evidence

        - moderate:
          Partial coverage with some noticeable skill or experience gaps

        - weak:
          Many important requirements are missing or unsupported
    """

    return system_prompt, user_prompt

def build_match_suggestions_prompt(match_input: dict):
    system_prompt = """
        You are a career advisor.

        You give actionable career advice.

        Rules:
        - Return ONLY valid JSON
        - Be specific and actionable
        - Avoid generic advice
        - Focus only on improvements
    """

    user_prompt = f"""
        Input:
        {match_input}

        Task:
        Provide exactly 3 to 5 high-impact improvement strings for the candidate.

        Return ONLY a JSON object with this exact schema:
        {{
            "actions": ["string", "string", "string"]
        }}

        Critical Rules:
        - The "actions" array must contain ONLY plain strings.
        - DO NOT use keys like "step_1" or "reasoning".
        - DO NOT include any text outside of the JSON block.
        - Each string must be under 15 words.
    """
    
    return system_prompt, user_prompt