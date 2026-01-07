# 🧩 Low-Level Design (LLD) — Cricket Live Platform

## 1. Purpose

This document describes the **internal design** of the Cricket Live Platform, including:

* Service responsibilities
* Data models (entities)
* Redis key design
* Internal data flows
* Code-level boundaries

This LLD is **directly implementable** and maps cleanly to the codebase.

---

## 2. Service Breakdown

### 2.1 Auth Service (Module)

**Responsibilities**

* JWT creation and validation
* Role-based authorization
* Token expiry and refresh handling

**Key Components**

* `JWTService`
* `AuthMiddleware`

---

### 2.2 Match Service

**Responsibilities**

* Create and manage matches
* Update match metadata
* Control match lifecycle

**Core Methods**

* `create_match()`
* `update_match()`
* `start_match()`
* `complete_match()`

---

### 2.3 Live Scoring Service

**Responsibilities**

* Accept ball-by-ball updates
* Update live state in Redis
* Publish events via Redis Pub/Sub
* Persist data asynchronously

**Core Methods**

* `add_ball_event()`
* `add_wicket_event()`
* `update_over()`

---

### 2.4 WebSocket Service

**Responsibilities**

* Manage active WebSocket connections
* Subscribe users to match channels
* Broadcast real-time updates
* Handle disconnects and reconnects

**Key Components**

* `ConnectionManager`
* `MatchChannelManager`

---

### 2.5 History Service

**Responsibilities**

* Serve completed match data
* Fetch scorecards and summaries
* Provide paginated ball-by-ball history

---

## 3. Entity Design (Database Models)

### 3.1 User

```text
User
----
id (UUID)
email
hashed_password
role (ADMIN | USER)
created_at
```

---

### 3.2 Match

```text
Match
-----
id (UUID)
team_a
team_b
venue
overs
status (SCHEDULED | LIVE | COMPLETED)
start_time
end_time
```

---

### 3.3 BallEvent

```text
BallEvent
---------
id (UUID)
match_id (FK)
over_number
ball_number
runs
extras
wicket (boolean)
created_at
```

---

### 3.4 Scorecard (Derived Entity)

```text
Scorecard
---------
match_id
total_runs
total_wickets
current_over
```

⚠️ **Note:**
`Scorecard` is **derived from `BallEvent`** and cached in Redis for fast access.

---

## 4. Redis Design (Live State)

### 4.1 Redis Keys

| Key                      | Type    | Description                 |
| ------------------------ | ------- | --------------------------- |
| `match:{id}:state`       | Hash    | Current score & match state |
| `match:{id}:events`      | List    | Recent ball events          |
| `match:{id}:subscribers` | Set     | Active WebSocket users      |
| `match:{id}:channel`     | Pub/Sub | Live match updates          |

---

### 4.2 Redis Data Example

```json
{
  "runs": 145,
  "wickets": 6,
  "overs": "18.3"
}
```

---

## 5. Internal Data Flow

### 5.1 Ball Update Flow (Admin → Users)

1. Admin sends REST request
2. Auth middleware validates JWT & role
3. Live Scoring Service updates Redis
4. Event published to Redis Pub/Sub
5. WebSocket Service broadcasts update
6. Event persisted to PostgreSQL asynchronously

---

### 5.2 WebSocket Subscription Flow

1. User establishes WebSocket connection
2. JWT validated
3. User subscribes to match channel
4. Initial state fetched from Redis
5. Live updates streamed in real time

---

## 6. Error Handling Strategy

| Scenario             | Action                    |
| -------------------- | ------------------------- |
| Invalid JWT          | `401 Unauthorized`        |
| Unauthorized role    | `403 Forbidden`           |
| Match not found      | `404 Not Found`           |
| Redis failure        | Fallback to DB            |
| WebSocket disconnect | Retry / reconnect support |

---

## 7. Concurrency & Consistency

* Single writer (admin) per match
* Redis atomic operations
* Optimistic writes to DB
* Idempotent event creation

---

## 8. Database Transactions

* Match updates executed in a single transaction
* Ball events written atomically
* Rollback on failure

---

## 9. Logging Strategy

* Structured logs (JSON)
* Correlation ID per request
* Separate log streams for:

  * REST APIs
  * WebSockets
  * Redis interactions

---

## 10. Testing Strategy (LLD View)

| Layer     | Test Type         |
| --------- | ----------------- |
| Services  | Unit tests        |
| API       | Integration tests |
| Redis     | Mocked tests      |
| WebSocket | Connection tests  |

---

## 11. Mapping to Code Structure

```text
backend/app/
├── api/
│   ├── auth.py
│   ├── matches.py
│   ├── scoring.py
│   └── ws.py
├── core/
│   ├── config.py
│   ├── security.py
├── models/
│   ├── user.py
│   ├── match.py
│   └── ball_event.py
├── services/
│   ├── auth_service.py
│   ├── match_service.py
│   ├── scoring_service.py
│   └── ws_service.py
```

---

## 12. Design Trade-offs

| Decision            | Reason                 |
| ------------------- | ---------------------- |
| Redis live state    | Ultra-low latency      |
| Async DB writes     | Faster user experience |
| Stateless WebSocket | Horizontal scalability |
| Derived scorecard   | Avoid recomputation    |

---

## 13. What This Enables

This LLD enables:

* Clean and predictable API contracts
* Well-defined Redis usage
* Safe concurrent updates
* Fast onboarding for new developers


