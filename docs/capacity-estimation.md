# 📊 Capacity Estimation & Scaling Strategy — Cricket Live Platform

## 1. Purpose

This document estimates **traffic, storage, memory, and compute requirements** for the Cricket Live Platform and defines a **scaling strategy** to reliably handle peak loads during live matches.

---

## 2. Assumptions

### Traffic Assumptions (Peak Event)

* Concurrent live matches: **50**
* Average concurrent users per match: **20,000**
* Peak concurrent users (total): **1,000,000**
* Admin scorers per match: **2**
* Average match duration: **3 hours**

---

## 3. Read & Write Patterns

### 3.1 Write Traffic (Admin Scoring)

* Ball updates per over: **6**
* Overs per match: **50**
* Total balls per match: **300**
* Events per match: **~350** (balls, wickets, extras)

**Peak Write Rate**

```
50 matches × 1 ball update / 30 seconds ≈ 1.6 writes/sec
```

➡️ **Write traffic is extremely low and easy to scale**

---

### 3.2 Read Traffic (Users)

#### REST API Reads

* Initial match load per user
* Assume **1 REST call per user**

```
1,000,000 users / 10 minutes ≈ 1,666 RPS
```

---

#### WebSocket Messages

* Every ball update is broadcasted

```
50 matches × 1 update / 30 seconds ≈ 1.6 events/sec
```

Each event fan-outs to:

* **20,000 users per match**

➡️ **WebSocket fan-out is the dominant load, not REST APIs**

---

## 4. WebSocket Capacity

### Concurrent Connections

* Peak WebSocket connections: **1,000,000**

### Backend Instance Capacity

* Conservative estimate: **50,000 connections / instance**

```
1,000,000 / 50,000 = 20 instances
```

➡️ **Provision 25 instances for safety buffer**

---

## 5. Redis Capacity Estimation

### 5.1 Key Count

| Key Type        | Per Match | Total    |
| --------------- | --------- | -------- |
| Live state      | 1         | 50       |
| Event list      | 1         | 50       |
| Subscribers set | 1         | 50       |
| Rate-limit keys | ~10,000   | ~500,000 |

---

### 5.2 Memory Usage

#### Live Match State

* ~1 KB per match → **50 KB**

#### Recent Events

* 100 events × 300 bytes ≈ **30 KB per match**
* 50 matches → **1.5 MB**

#### Rate Limiting

* ~100 bytes per key × 500K keys → **~50 MB**

---

### Total Redis Memory

➡️ **~100 MB**

**Provisioning Recommendation**

* Redis instance size: **512 MB – 1 GB**

---

## 6. PostgreSQL Storage Estimation

### Ball Events

* Events per match: **350**
* Matches per day: **100**
* Events per day: **35,000**

### Yearly Storage

```
35,000 × 365 ≈ 12.7 million rows
```

### Row Size

* ~300 bytes per row

```
12.7M × 300B ≈ 3.8 GB per year
```

➡️ **PostgreSQL can easily handle this with proper indexing**

---

## 7. API Throughput

### REST APIs

* Peak traffic: **~2,000 RPS**
* FastAPI capacity: **5–10K RPS per instance**

➡️ **5–6 API instances are sufficient**

---

## 8. Scaling Strategy

### 8.1 Horizontal Scaling

| Component         | Strategy               |
| ----------------- | ---------------------- |
| API servers       | Stateless, auto-scaled |
| WebSocket servers | Redis Pub/Sub          |
| Redis             | Primary + replica      |
| Database          | Read replicas          |

---

### 8.2 Autoscaling Triggers

* CPU usage > 70%
* Active WebSocket connections
* Redis memory utilization
* API response latency

---

## 9. Fault Tolerance

| Failure               | Handling                |
| --------------------- | ----------------------- |
| API instance crash    | Load balancer reroutes  |
| WebSocket server down | Client auto-reconnect   |
| Redis unavailable     | Fallback to database    |
| Database unavailable  | Read-only degraded mode |

---

## 10. Cost Awareness (Rough)

| Component         | Cost              |
| ----------------- | ----------------- |
| API instances     | Medium            |
| Redis             | Low               |
| Database          | Medium            |
| Network bandwidth | High (WebSockets) |

➡️ **WebSocket traffic is the dominant cost driver**

---

## 11. Bottlenecks & Mitigation

| Bottleneck        | Mitigation          |
| ----------------- | ------------------- |
| WebSocket fan-out | Horizontal scaling  |
| Redis Pub/Sub     | Sharding by match   |
| Database writes   | Async batching      |
| Cold starts       | Warm instance pools |

---

## 12. Trade-offs

| Decision             | Reason                    |
| -------------------- | ------------------------- |
| WebSockets           | True real-time experience |
| Redis                | Ultra-low latency         |
| Eventual consistency | Higher throughput         |

---

## 13. Final Summary

* Write load is minimal
* Read traffic and fan-out dominate
* Redis is a critical dependency
* WebSockets define system scale
* Architecture comfortably supports **10× growth**

---

