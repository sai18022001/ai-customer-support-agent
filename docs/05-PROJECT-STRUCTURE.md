# Project Structure

```
ai-customer-support-agent/
│
├── docs/                           # Documentation
│   ├── 01-PROJECT-OVERVIEW.md
│   ├── 02-ARCHITECTURE.md
│   ├── 03-DATABASE-SCHEMA.md
│   ├── 04-API-SPECIFICATION.md
│   └── 05-PROJECT-STRUCTURE.md
│
├── app/                            # Main application package
│   ├── __init__.py
│   ├── main.py                     # FastAPI app entry point
│   ├── config.py                   # Configuration & environment variables
│   │
│   ├── models/                     # SQLAlchemy database models
│   │   ├── __init__.py
│   │   ├── customer.py
│   │   ├── order.py
│   │   ├── product.py
│   │   ├── case.py
│   │   ├── session.py
│   │   ├── message.py
│   │   └── action.py
│   │
│   ├── schemas/                    # Pydantic request/response schemas
│   │   ├── __init__.py
│   │   ├── customer.py
│   │   ├── order.py
│   │   ├── case.py
│   │   ├── chat.py
│   │   └── analytics.py
│   │
│   ├── api/                        # API route handlers
│   │   ├── __init__.py
│   │   ├── router.py               # Main router aggregator
│   │   ├── chat.py                 # POST /chat endpoints
│   │   ├── customers.py            # CRUD customer endpoints
│   │   ├── orders.py               # CRUD order endpoints
│   │   ├── cases.py                # CRUD case endpoints
│   │   └── analytics.py            # Analytics endpoints
│   │
│   ├── services/                   # Business logic layer
│   │   ├── __init__.py
│   │   ├── ai_engine.py            # LLM integration — intent, sentiment, response
│   │   ├── crm_service.py          # Customer/order data operations
│   │   ├── case_service.py         # Case lifecycle management
│   │   ├── action_executor.py      # Execute AI-planned actions
│   │   └── analytics_service.py    # Metrics aggregation
│   │
│   ├── core/                       # Cross-cutting concerns
│   │   ├── __init__.py
│   │   ├── database.py             # DB engine, session factory
│   │   ├── auth.py                 # API key authentication
│   │   └── exceptions.py           # Custom exception classes
│   │
│   └── seed/                       # Sample data for development
│       ├── __init__.py
│       └── seed_data.py            # Seed customers, orders, products
│
├── tests/                          # Test suite
│   ├── __init__.py
│   ├── conftest.py                 # Shared fixtures
│   ├── test_chat.py                # Chat endpoint tests
│   ├── test_customers.py           # Customer CRUD tests
│   ├── test_orders.py              # Order CRUD tests
│   ├── test_cases.py               # Case management tests
│   ├── test_ai_engine.py           # AI engine unit tests
│   └── test_analytics.py           # Analytics tests
│
├── .env.example                    # Environment variable template
├── .gitignore
├── requirements.txt        on dependencies
├── Dockerfile                      # Container definition
├── docker-compose.yml              # Multi-service orchestration
├── pytest.ini                      # Test configuration
└── README.md                       # Project README
```

## Module Responsibilities

### `app/models/` — Database Models
SQLAlchemy ORM models that map to database tables. Each model defines columns, relationships, and constraints.

### `app/schemas/` — Pydantic Schemas
Request validation and response serialization. Separates API contract from database structure.

### `app/api/` — Route Handlers
Thin controllers that validate input, call services, and return responses. No business logic here.

### `app/services/` — Business Logic
Where the real work happens. Services are independent, testable, and reusable.

### `app/core/` — Infrastructure
Database connections, authentication, error handling — shared across all modules.

### `tests/` — Test Suite
Mirrors the app structure. Uses pytest fixtures for database setup/teardown.
