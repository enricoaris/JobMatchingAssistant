# Resume-Job Matching Engine

AI-powered tool that matches resumes to job descriptions using semantic similarity and LLMs.

## Demo Video

[Link to video]

## Features

- Upload resumes (PDF/DOCX) and job descriptions
- Semantic similarity matching using LLMs
- Asynchronous processing with RabbitMQ
- Real-time progress updates via SignalR
- Pluggable LLM architecture (local or cloud providers)
- Match scoring with keyword highlighting

## Tech Stack

**Backend API:** .NET (C#)  
**AI Service:** Python (consumes RabbitMQ events)  
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