# Resume-Job Matching Engine

End-to-end system that extracts and matches skills from resumes and job descriptions using LLMs and semantic similarity.

## Demo Video
[https://youtu.be/pS8qNTXYTX4]

## Features
- Analyze resumes and job descriptions using Large Language Models (LLMs)
- Extract skills, experience, highlights, and job requirements
- Hybrid extraction using LLMs and a rule-based skills dictionary
- Generate semantic embeddings for resumes and job descriptions
- Match resumes to jobs using vector similarity
- Generate AI-powered match summaries and recommendations
- Extract text from PDF resumes
- Process documents asynchronously using background workers
- Support pluggable LLM providers (local or cloud)
- Mock mode for development and demonstrations

## Tech Stack
**Backend API:** .NET (C#)  
**AI Service:** Python (LLM integration, embedding generation)  
**Frontend:** React, TypeScript, MUI  
**Message Queue:** RabbitMQ  
**Real-time:** SignalR  
**Database:** PostgreSQL  

## Quick Start

### Prerequisites
- Docker and Docker Compose

### Run with Docker
```bash
# Clone the repository
git clone https://github.com/enricoaris/resume-matcher
cd resume-matcher

# Copy environment variables
cp .env.example .env

# Start all services
docker-compose up --build

# Access the application
http://localhost:5173