# System Architecture

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        CLIENTS                                  │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────┐  │
│  │  Chat Widget  │  │  REST API    │  │  Analytics Dashboard │  │
│  │  (React)      │  │  (Postman)   │  │  (React + Charts)    │  │
│  └──────┬───────┘  └──────┬───────┘  └──────────┬───────────┘  │
└─────────┼─────────────────┼─────────────────────┼───────────────┘
          │                 │                     │
          ▼                 ▼                     ▼
┌─────────────────────────────────────────────────────────────────┐
│                      API GATEWAY (FastAPI)                       │
│  ┌─────────────┐  ┌──────────────┐  ┌────────────────────────┐ │
│  │ /chat       │  │ /customers   │  │ /analytics             │ │
│  │ /cases      │  │ /orders      │  │ /health                │ │
│  └──────┬──────┘  └──────┬───────┘  └────────────┬───────────┘ │
│         │                │                       │              │
│  ┌──────▼────────────────▼───────────────────────▼───────────┐  │
│  │              Authentication & Rate Limiting               │  │
│  └───────────────────────┬───────────────────────────────────┘  │
└──────────────────────────┼──────────────────────────────────────┘
                           │
          ┌────────────────┼────────────────┐
          ▼                ▼                ▼
┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│  AI ENGINE   │  │  CRM SERVICE │  │  CASE SERVICE│
│              │  │              │  │              │
│ - Intent     │  │ - Customers  │  │ - Create     │
│   Detection  │  │ - Orders     │  │ - Update     │
│ - Response   │  │ - Products   │  │ - Escalate   │
│   Generation │  │ - History    │  │ - Resolve    │
│ - Sentiment  │  │              │  │              │
│   Analysis   │  │              │  │              │
│ - Action     │  │              │  │              │
│   Planning   │  │              │  │              │
└──────┬───────┘  └──────┬───────┘  └──────┬───────┘
       │                 │                 │
       ▼                 ▼                 ▼
┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│  Gemini API  │  │  Database    │  │  Task Queue  │
│  (LLM)       │  │  (SQLite/    │  │  (Celery +   │
│              │  │   PostgreSQL)│  │   Redis)     │
└──────────────┘  └──────────────┘  └──────────────┘
```

## Component Details

### 1. API Gateway (FastAPI)

The entry point for all client requests. Responsibilities:
- Route requests to appropriate services
- Authentication via API keys
- Rate limiting (per-client token bucket)
- Request validation (Pydantic models)
- CORS handling for frontend

### 2. AI Engine

The brain of the system. Processes customer messages through a pipeline:

```
Customer Message
       │
       ▼
┌──────────────┐
│   Intent     │──── billing / technical / account / general / escalate
│   Classifier │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│  Sentiment   │──── positive / neutral / negative / angry
│  Analyzer    │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│   Action     │──── lookup_order / create_case / update_account / escalate
│   Planner    │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│  Action      │──── Executes planned actions against CRM
│  Executor    │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│  Response    │──── Generates natural language response
│  Generator   │
└──────────────┘
```

### 3. CRM Service

Manages all customer-related data:
- **Customers**: Profile, contact info, tier (basic/premium/enterprise)
- **Orders**: Order history, status, tracking
- **Products**: Product catalog, pricing
- **Interactions**: Full conversation history

### 4. Case Management Service

Handles support ticket lifecycle:
- **Create**: New case from AI-detected issues
- **Update**: Status changes, notes, assignments
- **Escalate**: Route to human agent with full context
- **Resolve**: Close case with resolution summary
- **SLA Tracking**: Priority-based response time targets

### 5. Analytics Service

Aggregates and serves operational metrics:
- Resolution rate (AI vs human)
- Average response time
- Customer satisfaction scores
- Intent distribution
- Escalation rate trends

## Data Flow — Chat Interaction

```
1. Customer sends message via chat widget
2. FastAPI receives POST /api/v1/chat
3. AI Engine pipeline:
   a. Classify intent (billing? technical? account?)
   b. Analyze sentiment (is customer frustrated?)
   c. Plan actions (need to look up order? create case?)
   d. Execute actions (query CRM database)
   e. Generate response (natural language with context)
4. Response returned to customer
5. Conversation stored in database
6. Metrics updated (Prometheus counters)
```

## Data Flow — Escalation

```
1. AI detects escalation trigger:
   - Sentiment = angry for 2+ consecutive messages
   - Customer explicitly asks for human
   - Confidence score < 0.6
   - Issue complexity exceeds AI capability
2. Case created with full conversation history
3. Case assigned to available human agent
4. Customer notified of handoff
5. Human agent gets full context (no repeat explanations)
```
