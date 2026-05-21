PROGRAMMING = {
    "python": ["python", "py"],
    "javascript": ["javascript", "js"],
    "typescript": ["typescript", "ts"],
    "java": ["java"],
    "c#": ["c#", "csharp", ".net"],
    "c++": ["c++"],
    "c": ["c"],
    "go": ["go", "golang"],
    "rust": ["rust"],
    "php": ["php"],
    "ruby": ["ruby"],
    "swift": ["swift"],
    "kotlin": ["kotlin"],
    "r": ["r"],
    "matlab": ["matlab"],
}

FRONTEND = {
    "react": ["react", "react.js"],
    "angular": ["angular"],
    "vue": ["vue", "vue.js"],
    "html": ["html"],
    "css": ["css"],
    "tailwind": ["tailwind", "tailwindcss"],
    "bootstrap": ["bootstrap"],
    "next.js": ["next.js", "nextjs"],
}

BACKEND = {
    "node.js": ["node.js", "nodejs"],
    "express": ["express", "express.js"],
    "django": ["django"],
    "flask": ["flask"],
    "spring": ["spring", "spring boot"],
    ".net": [".net", "asp.net", "aspnet"],
    "fastapi": ["fastapi"],
    "laravel": ["laravel"],
}

DATABASES = {
    "postgresql": ["postgresql", "postgres"],
    "mysql": ["mysql"],
    "mongodb": ["mongodb", "mongo"],
    "redis": ["redis"],
    "sqlite": ["sqlite"],
    "oracle": ["oracle"],
    "sql server": ["sql server", "mssql"],
}

DEVOPS = {
    "aws": ["aws", "amazon web services"],
    "azure": ["azure"],
    "gcp": ["gcp", "google cloud"],
    "docker": ["docker"],
    "kubernetes": ["kubernetes", "k8s"],
    "terraform": ["terraform"],
    "ci/cd": ["ci/cd", "continuous integration"],
    "jenkins": ["jenkins"],
    "nginx": ["nginx"],
}

AI_ML = {
    "machine learning": ["machine learning", "ml"],
    "deep learning": ["deep learning"],
    "pytorch": ["pytorch"],
    "tensorflow": ["tensorflow"],
    "scikit-learn": ["scikit-learn", "sklearn"],
    "pandas": ["pandas"],
    "numpy": ["numpy"],
    "nlp": ["nlp", "natural language processing"],
}

TOOLS = {
    "git": ["git"],
    "github": ["github"],
    "gitlab": ["gitlab"],
    "jira": ["jira"],
    "figma": ["figma"],
    "postman": ["postman"],
    "linux": ["linux"],
    "bash": ["bash", "shell"],
}

SKILLS = {
    **PROGRAMMING,
    **FRONTEND,
    **BACKEND,
    **DATABASES,
    **DEVOPS,
    **AI_ML,
    **TOOLS,
}