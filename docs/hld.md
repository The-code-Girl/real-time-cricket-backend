# 📐 High-Level Design (HLD) — Cricket Live Platform

## 1. Purpose

This document describes the **high-level architecture** of the Cricket Live Platform, covering:

* Major system components
* Data flow
* Technology choices
* Scalability and reliability considerations

It acts as a bridge between **requirements** and **low-level design (LLD)**.

---

## 2. System Overview

The platform is a **real-time, event-driven backend system** where:

* **Admins** publish live cricket match events
* **Users** consume real-time updates via **WebSockets**
* **Redis** acts as the real-time backbone
* **PostgreSQL** stores durable match data

**Key Characteristics**

* Stateless services
* Horizontally scalable
* Cloud-native & production-ready

---

## 3. High-Level Architecture (Logical View)

```text
┌────────────┐
│  Clients   │
│ (Web/Mobile)│
└─────┬──────┘
      │
┌─────▼────────┐
│ Load Balancer │
└─────┬────────┘
      │
┌─────▼──────────────────┐
│   FastAPI Backend       │
│ (REST + WebSocket APIs) │
└─────┬─────────┬────────┘
      │         │
┌─────▼───┐ ┌───▼────────┐
│PostgreSQL│ │   Redis   │
│(History) │ │ Cache +   │
│          │ │ Pub/Sub  │
└──────────┘ └───────────┘
```

---

## 4. Core Components

### 4.1 Backend Service (FastAPI)

**Responsibilities**

* REST APIs (auth, match management, history)
* WebSocket connection handling
* JWT validation
* Role-based access control (RBAC)
* Redis event publish/consume

**Why FastAPI**

* Async-first (ideal for WebSockets)
* High throughput
* Clean dependency injection
* Auto-generated API documentation

---

### 4.2 WebSocket Manager

**Responsibilities**

* Maintain active WebSocket connections
* Map users to match subscriptions
* Broadcast live updates
* Handle reconnects gracefully

**Design Characteristics**

* Stateless
* Horizontally scalable
* Uses Redis Pub/Sub for cross-instance messaging

---

### 4.3 Redis

**Usage**

* Live match state caching
* Pub/Sub for real-time events
* Temporary data with TTL

**Why Redis**

* Extremely low latency
* Native Pub/Sub support
* Shared state across backend instances
* Reduces PostgreSQL load

---

### 4.4 PostgreSQL

**Responsibilities**

* Persistent storage for:

  * Matches
  * Teams
  * Players
  * Ball-by-ball history
* Source of truth for completed matches

**Design Choice**

* Strong consistency
* ACID compliance
* Mature indexing & migration support

---

### 4.5 Authentication & Authorization

* JWT-based authentication
* Role-based access control:

  * `ADMIN`
  * `USER`
* Middleware-level enforcement

---

## 5. Data Flow

### 5.1 Live Match Update Flow (Admin → Users)

1. Admin sends ball update via REST API
2. Backend validates:

   * JWT
   * Admin role
3. Live state written to Redis
4. Event published to Redis Pub/Sub
5. All WebSocket servers receive the event
6. Update broadcast to subscribed users
7. Periodic persistence to PostgreSQL

---

### 5.2 User Subscription Flow

1. User establishes WebSocket connection
2. JWT validated
3. User subscribes to a match channel
4. Initial match state fetched from Redis
5. Live updates streamed in real time

---

### 5.3 Match Completion Flow

1. Admin marks match as completed
2. Final state persisted to PostgreSQL
3. Redis cache invalidated (or TTL expiry)
4. WebSocket channels closed gracefully

---

## 6. Scalability Strategy

### 6.1 Horizontal Scaling

* Backend instances are stateless
* WebSockets scale via Redis Pub/Sub
* Load balancer distributes traffic

### 6.2 Read Optimization

* Live reads → Redis
* Historical reads → PostgreSQL
* Protects DB from read spikes

### 6.3 Write Optimization

* Admin writes are low volume
* Writes are validated and serialized
* Optional batched DB writes

---

## 7. Fault Tolerance

| Component  | Strategy                  |
| ---------- | ------------------------- |
| Backend    | Multiple instances        |
| Redis      | Replication + persistence |
| PostgreSQL | Backups + failover        |
| WebSockets | Client reconnect support  |

---

## 8. Security Considerations

* HTTPS everywhere
* Secure WebSockets (`wss`)
* JWT expiry & refresh strategy
* Rate limiting on REST APIs
* Strict input validation

---

## 9. Deployment Overview

* Dockerized services
* Docker Compose (local development)
* Kubernetes-ready architecture
* Environment-based configuration

---

## 10. Trade-offs & Key Decisions

| Decision           | Reason                  |
| ------------------ | ----------------------- |
| Redis Pub/Sub      | Simplicity + speed      |
| PostgreSQL         | Strong consistency      |
| FastAPI            | Async performance       |
| Stateless services | Easy horizontal scaling |

---

## 11. What This Enables

* Clean Low-Level Design (LLD)
* Clear API contracts
* Confident capacity estimation
* Interview-ready system explanation

