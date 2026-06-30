# AI Customer Support Agent

An autonomous AI-powered customer support agent that handles customer queries end-to-end — classifies intent, analyzes sentiment, takes CRM actions, and generates contextual responses. Inspired by **Salesforce Agentforce**.

## Features

- **AI-Powered Conversations** — Uses Google Gemini to understand and respond to customer queries
- **Intent Classification** — Automatically detects billing, technical, order, and account inquiries
- **Sentiment Analysis** — Monitors customer mood and triggers escalation when needed
- **Autonomous Actions** — Looks up orders, creates support cases, and updates accounts without human intervention
- **CRM Integration** — Full customer, order, and case management system
- **Smart Escalation** — Routes complex or high-emotion cases to human agents with full context
- **Analytics API** — Resolution rates, intent distribution, satisfaction metrics
- **REST API** — Complete API with Swagger documentation

## Tech Stack

Python, FastAPI, SQLAlchemy, SQLite, Google Gemini AI, Pydantic, pytest

## Quick Start

```bash
python -m venv venv
venv\Scripts\activate          # Windows
pip install -r requirements.txt
cp .env.example .env           # Add your GEMINI_API_KEY
python -m app.seed.seed_data   # Load sample data
uvicorn app.main:app --reload
```

Open http://localhost:8000/docs for interactive API docs.

## Run Tests

```bash
pytest
pytest --cov=app --cov-report=html
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /api/v1/chat | Send message to AI agent |
| GET | /api/v1/chat/sessions/{id} | Get conversation history |
| GET/POST | /api/v1/customers | List/Create customers |
| GET/POST | /api/v1/orders | List/Create orders |
| GET/POST | /api/v1/cases | List/Create support cases |
| GET | /api/v1/analytics/overview | Dashboard metrics |
| GET | /api/v1/analytics/intents | Intent distribution |

## Architecture

See [docs/02-ARCHITECTURE.md](docs/02-ARCHITECTURE.md) for full system design.
