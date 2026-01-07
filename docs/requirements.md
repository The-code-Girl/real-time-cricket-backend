# 📄 Requirements — Cricket Live Platform

## 1. Overview

The **Cricket Live Platform** is a real-time system that allows **admins/scorers** to publish live cricket match events while **users** consume instant, ball-by-ball updates with minimal latency.

The platform is designed to be:

* Scalable
* Fault-tolerant
* Production-ready

It must handle **high traffic spikes** during popular live matches.

---

## 2. Goals

* Deliver real-time match updates with **low latency**
* Support **high concurrency** during live matches
* Maintain **accurate historical match data**
* Enforce **role-based access control**
* Be **cloud-ready** and horizontally scalable
* Follow clean architecture and industry best practices

---

## 3. User Roles

### 3.1 Admin (Scorer / Match Official)

**Capabilities**

* Create and manage matches
* Publish live match events:

  * Ball
  * Runs
  * Wickets
  * Overs
* Control match lifecycle:

  * Start
  * Pause
  * Finish

---

### 3.2 User (Viewer)

**Capabilities**

* View live match scores
* Subscribe to real-time updates
* View completed match history
* Read-only access

---

## 4. Functional Requirements

### 4.1 Authentication & Authorization

* System shall support **JWT-based authentication**
* Role-based authorization:

  * `ADMIN`
  * `USER`
* Only admins can:

  * Create matches
  * Update live match data

---

### 4.2 Match Management

* Admin can create a match
* Admin can update match metadata:

  * Teams
  * Venue
  * Overs
  * Match status:

    * `SCHEDULED`
    * `LIVE`
    * `COMPLETED`

---

### 4.3 Live Scoring

* Admin can publish **ball-by-ball updates**:

  * Runs
  * Extras
  * Wickets
  * Over completion
* Each update must:

  * Be processed immediately
  * Reflect in real time to all subscribed users

---

### 4.4 Real-Time Updates

* Users receive live updates via **WebSockets**
* System must support **thousands of concurrent WebSocket connections**
* Updates must be:

  * Ordered
  * Consistent per match

---

### 4.5 Match History

* Completed matches must be stored permanently
* Users can fetch:

  * Match summary
  * Scorecards
  * Ball-by-ball history

    * Optional pagination for large matches

---

### 4.6 Caching

* Live match state must be cached in **Redis**
* Database must not be hit for every live update
* Cache should:

  * Be invalidated
  * Or expire via TTL after match completion

---

### 4.7 Observability

* Structured logging
* Centralized error handling
* Meaningful and consistent HTTP error responses

---

## 5. Non-Functional Requirements

### 5.1 Performance

* Live update latency: **< 500 ms**
* API response time: **< 200 ms (P95)**
* WebSocket fan-out must scale horizontally

---

### 5.2 Scalability

System must support:

* **100K+ concurrent users**
* **10K+ updates per minute** during peak matches

Architecture requirements:

* Stateless API servers
* Horizontal scaling via load balancer

---

### 5.3 Availability

* Target availability: **99.9%**
* Redis or DB failures should not crash the system
* Graceful degradation for non-critical features

---

### 5.4 Consistency

* **Strong consistency** for admin writes
* **Eventual consistency** acceptable for user views
  *(milliseconds-level delay)*

---

### 5.5 Security

* JWT validation on all protected endpoints
* Rate limiting on REST APIs
* Secure WebSocket connections (`wss`)
* Input validation and sanitization

---

### 5.6 Maintainability

* Clean separation of concerns
* Modular architecture
* Well-documented APIs and code
* Database migrations via **Alembic**

---

## 6. Out of Scope (Initial Phase)

* Video streaming
* Betting or fantasy league features
* AI-based predictions
* Multi-language UI

---

## 7. Assumptions

* A single match has limited admins (1–5)
* Majority of traffic is **read-heavy**
* Users primarily consume live data
* Writes are significantly lower than reads

---

## 8. Future Enhancements

* Multiple simultaneous live matches
* Push notifications
* Match analytics
* Leaderboards and player statistics

---

## 9. Success Metrics

* Real-time updates delivered within SLA
* Zero data loss for match events
* Stable performance during peak traffic
* Easy onboarding for new developers

---

## ✅ Status

This document serves as the foundation for:

* High-Level Design (HLD)
* Low-Level Design (LLD)
* API contracts
* Capacity estimation


