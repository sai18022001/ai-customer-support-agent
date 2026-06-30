# Setup & Development Guide

## Prerequisites

- Python 3.11+
- Git
- Google Gemini API key (free tier available at https://aistudio.google.com/apikey)

## Quick Start

### 1. Clone & Setup Virtual Environment

```bash
cd ai-customer-support-agent

# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (Mac/Linux)
source venv/bin/activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment

```bash
# Copy the example env file
cp .env.example .env

# Edit .env and add your Gemini API key
# GEMINI_API_KEY=your-key-here
```

### 4. Seed the Database

```bash
python -m app.seed.seed_data
```

### 5. Run the Server

```bash
uvicorn app.main:app --reload --port 8000
```

### 6. Verify

Open http://localhost:8000/docs to see the interactive API documentation (Swagger UI).

## Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app --cov-report=html

# Run specific test file
pytest tests/test_chat.py -v
```

## Project Structure at a Glance

```
app/
├── main.py          ← Start here: FastAPI app setup
├── config.py        ← Environment variables
├── models/          ← Database tables (SQLAlchemy)
├── schemas/         ← Request/Response models (Pydantic)
├── api/             ← HTTP endpoints
├── services/        ← Business logic + AI engine
└── core/            ← Database, auth, error handling
```

## Key Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| GEMINI_API_KEY | Yes | — | Google Gemini API key |
| DATABASE_URL | No | sqlite:///./agent.db | Database connection string |
| API_KEY | No | dev-api-key-123 | API authentication key |
| LOG_LEVEL | No | INFO | Logging level |
| ENVIRONMENT | No | development | development / production |
