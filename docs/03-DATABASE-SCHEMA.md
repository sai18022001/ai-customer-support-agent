# Database Schema

## Entity Relationship Diagram

```
┌──────────────┐       ┌──────────────┐       ┌──────────────┐
│  customers   │       │   orders     │       │  products    │
├──────────────┤       ├──────────────┤       ├──────────────┤
│ id (PK)      │──┐    │ id (PK)      │    ┌──│ id (PK)      │
│ name         │  │    │ customer_id  │──┘  │  │ name         │
│ email        │  │    │ product_id   │─────┘  │ category     │
│ phone        │  │    │ status       │        │ price        │
│ tier         │  │    │ total_amount │        │ description  │
│ company      │  │    │ created_at   │        │ created_at   │
│ created_at   │  │    │ updated_at   │        └──────────────┘
│ updated_at   │  │    └──────────────┘
└──────────────┘  │
                  │    ┌──────────────┐       ┌──────────────┐
                  │    │   cases      │       │  messages    │
                  │    ├──────────────┤       ├──────────────┤
                  ├───▶│ id (PK)      │    ┌──│ id (PK)      │
                  │    │ customer_id  │    │  │ session_id   │──┐
                  │    │ subject      │    │  │ role         │  │
                  │    │ description  │    │  │ content      │  │
                  │    │ status       │    │  │ intent       │  │
                  │    │ priority     │    │  │ sentiment    │  │
                  │    │ category     │    │  │ confidence   │  │
                  │    │ assigned_to  │    │  │ created_at   │  │
                  │    │ resolution   │    │  └──────────────┘  │
                  │    │ created_at   │    │                    │
                  │    │ resolved_at  │    │  ┌──────────────┐  │
                  │    │ updated_at   │    │  │  sessions    │  │
                  │    └──────────────┘    │  ├──────────────┤  │
                  │                       │  │ id (PK)      │◀─┘
                  │    ┌──────────────┐    │  │ customer_id  │
                  │    │  actions     │    │  │ status       │
                  │    ├──────────────┤    │  │ started_at   │
                  └───▶│ id (PK)      │    │  │ ended_at     │
                       │ session_id   │────┘  │ escalated    │
                       │ action_type  │       │ satisfaction │
                       │ parameters   │       └──────────────┘
                       │ result       │
                       │ status       │
                       │ created_at   │
                       └──────────────┘
```

## Table Definitions

### customers
| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PK | Unique customer identifier |
| name | VARCHAR(100) | NOT NULL | Full name |
| email | VARCHAR(255) | UNIQUE, NOT NULL | Email address |
| phone | VARCHAR(20) | | Phone number |
| tier | ENUM | DEFAULT 'basic' | basic / premium / enterprise |
| company | VARCHAR(200) | | Company name |
| created_at | TIMESTAMP | DEFAULT NOW() | Account creation date |
| updated_at | TIMESTAMP | | Last update timestamp |

### products
| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PK | Unique product identifier |
| name | VARCHAR(200) | NOT NULL | Product name |
| category | VARCHAR(100) | NOT NULL | Product category |
| price | DECIMAL(10,2) | NOT NULL | Unit price |
| description | TEXT | | Product description |
| created_at | TIMESTAMP | DEFAULT NOW() | Creation date |

### orders
| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PK | Unique order identifier |
| customer_id | UUID | FK → customers | Customer who placed order |
| product_id | UUID | FK → products | Product ordered |
| quantity | INTEGER | DEFAULT 1 | Quantity ordered |
| total_amount | DECIMAL(10,2) | NOT NULL | Total price |
| status | ENUM | DEFAULT 'pending' | pending / confirmed / shipped / delivered / cancelled |
| created_at | TIMESTAMP | DEFAULT NOW() | Order date |
| updated_at | TIMESTAMP | | Last status update |

### cases
| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PK | Unique case identifier |
| customer_id | UUID | FK → customers | Customer who raised case |
| subject | VARCHAR(300) | NOT NULL | Case subject line |
| description | TEXT | NOT NULL | Detailed description |
| status | ENUM | DEFAULT 'open' | open / in_progress / escalated / resolved / closed |
| priority | ENUM | DEFAULT 'medium' | low / medium / high / critical |
| category | VARCHAR(100) | | billing / technical / account / general |
| assigned_to | VARCHAR(100) | | Human agent name (if escalated) |
| resolution | TEXT | | Resolution summary |
| created_at | TIMESTAMP | DEFAULT NOW() | Case creation date |
| resolved_at | TIMESTAMP | | Resolution date |
| updated_at | TIMESTAMP | | Last update |

### sessions
| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PK | Unique session identifier |
| customer_id | UUID | FK → customers | Customer in this session |
| status | ENUM | DEFAULT 'active' | active / ended / escalated |
| started_at | TIMESTAMP | DEFAULT NOW() | Session start |
| ended_at | TIMESTAMP | | Session end |
| escalated | BOOLEAN | DEFAULT FALSE | Was this escalated? |
| satisfaction | INTEGER | | 1-5 rating (post-session) |

### messages
| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PK | Unique message identifier |
| session_id | UUID | FK → sessions | Parent session |
| role | ENUM | NOT NULL | customer / agent / system |
| content | TEXT | NOT NULL | Message content |
| intent | VARCHAR(50) | | Classified intent |
| sentiment | VARCHAR(20) | | Detected sentiment |
| confidence | FLOAT | | AI confidence score (0-1) |
| created_at | TIMESTAMP | DEFAULT NOW() | Message timestamp |

### actions
| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PK | Unique action identifier |
| session_id | UUID | FK → sessions | Session this action belongs to |
| action_type | VARCHAR(50) | NOT NULL | lookup_order / create_case / update_account / escalate |
| parameters | JSON | | Action parameters |
| result | JSON | | Action result/output |
| status | ENUM | DEFAULT 'pending' | pending / completed / failed |
| created_at | TIMESTAMP | DEFAULT NOW() | Action timestamp |
