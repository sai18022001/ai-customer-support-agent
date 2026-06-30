# API Specification

## Base URL
```
http://localhost:8000/api/v1
```

## Authentication
All endpoints require an API key in the header:
```
X-API-Key: your-api-key-here
```

---

## Chat Endpoints

### POST /chat
Send a message and receive AI agent response.

**Request:**
```json
{
  "customer_id": "uuid",
  "session_id": "uuid (optional — creates new session if omitted)",
  "message": "I need help with my recent order"
}
```

**Response:**
```json
{
  "session_id": "uuid",
  "response": "I'd be happy to help with your order. Could you provide your order number?",
  "intent": "order_inquiry",
  "sentiment": "neutral",
  "confidence": 0.92,
  "actions_taken": [
    {
      "type": "lookup_customer",
      "status": "completed"
    }
  ],
  "escalated": false
}
```

### GET /chat/sessions/{session_id}
Get full conversation history for a session.

**Response:**
```json
{
  "session_id": "uuid",
  "customer_id": "uuid",
  "status": "active",
  "messages": [
    {
      "id": "uuid",
      "role": "customer",
      "content": "I need help with my order",
      "intent": "order_inquiry",
      "sentiment": "neutral",
      "created_at": "2026-01-15T10:30:00Z"
    },
    {
      "id": "uuid",
      "role": "agent",
      "content": "I'd be happy to help...",
      "created_at": "2026-01-15T10:30:01Z"
    }
  ],
  "started_at": "2026-01-15T10:30:00Z"
}
```

---

## Customer Endpoints

### GET /customers
List all customers with optional filters.

**Query Parameters:**
| Param | Type | Description |
|-------|------|-------------|
| tier | string | Filter by tier (basic/premium/enterprise) |
| search | string | Search by name or email |
| page | int | Page number (default: 1) |
| limit | int | Items per page (default: 20, max: 100) |

### GET /customers/{customer_id}
Get customer profile with recent activity.

### POST /customers
Create a new customer.

### PUT /customers/{customer_id}
Update customer details.

---

## Order Endpoints

### GET /orders
List orders with filters.

**Query Parameters:**
| Param | Type | Description |
|-------|------|-------------|
| customer_id | uuid | Filter by customer |
| status | string | Filter by status |
| page | int | Page number |
| limit | int | Items per page |

### GET /orders/{order_id}
Get order details.

### POST /orders
Create a new order.

### PUT /orders/{order_id}
Update order status.

---

## Case Endpoints

### GET /cases
List support cases.

**Query Parameters:**
| Param | Type | Description |
|-------|------|-------------|
| customer_id | uuid | Filter by customer |
| status | string | Filter by status |
| priority | string | Filter by priority |
| category | string | Filter by category |

### GET /cases/{case_id}
Get case details with full history.

### POST /cases
Create a new support case.

### PUT /cases/{case_id}
Update case (status, assignment, resolution).

---

## Analytics Endpoints

### GET /analytics/overview
Get dashboard overview metrics.

**Response:**
```json
{
  "total_sessions": 1250,
  "ai_resolved": 980,
  "escalated": 270,
  "resolution_rate": 78.4,
  "avg_response_time_ms": 1200,
  "avg_satisfaction": 4.2,
  "active_sessions": 15
}
```

### GET /analytics/intents
Get intent distribution breakdown.

**Response:**
```json
{
  "intents": [
    {"intent": "billing", "count": 420, "percentage": 33.6},
    {"intent": "technical", "count": 350, "percentage": 28.0},
    {"intent": "order_inquiry", "count": 280, "percentage": 22.4},
    {"intent": "account", "count": 120, "percentage": 9.6},
    {"intent": "general", "count": 80, "percentage": 6.4}
  ]
}
```

### GET /analytics/trends
Get metrics over time.

**Query Parameters:**
| Param | Type | Description |
|-------|------|-------------|
| period | string | daily / weekly / monthly |
| days | int | Number of days to look back (default: 30) |

---

## Health Endpoint

### GET /health
System health check.

**Response:**
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "database": "connected",
  "llm_service": "connected",
  "uptime_seconds": 86400
}
```

---

## Error Responses

All errors follow this format:
```json
{
  "error": {
    "code": "CUSTOMER_NOT_FOUND",
    "message": "Customer with ID xyz not found",
    "status": 404
  }
}
```

### Error Codes
| HTTP Status | Code | Description |
|-------------|------|-------------|
| 400 | VALIDATION_ERROR | Invalid request body |
| 401 | UNAUTHORIZED | Missing or invalid API key |
| 404 | NOT_FOUND | Resource not found |
| 429 | RATE_LIMITED | Too many requests |
| 500 | INTERNAL_ERROR | Server error |
