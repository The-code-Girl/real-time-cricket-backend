# 🚀 Redis Design — Cricket Live Platform

## 1. Purpose

This document describes how **Redis** is used in the Cricket Live Platform to:

* Cache live match state
* Enable real-time pub/sub messaging
* Reduce primary database load
* Support horizontal scalability

Redis acts as the **real-time backbone** of the system.

---

## 2. Why Redis?

Redis is chosen for its ability to deliver real-time performance:

* Sub-millisecond latency
* In-memory data access
* Native Pub/Sub support
* Atomic operations
* TTL-based key eviction

---

## 3. Redis Use Cases

| Use Case         | Description                   |
| ---------------- | ----------------------------- |
| Live State Cache | Current score, overs, wickets |
| Pub/Sub          | Broadcast live match events   |
| Temporary Data   | Active subscriptions          |
| Rate Limiting    | Request throttling            |

---

## 4. Redis Key Design

### 4.1 Live Match State

* **Key**: `match:{match_id}:state`
* **Type**: `HASH`

**Fields**

* `runs`
* `wickets`
* `overs`
* `last_updated`

---

### 4.2 Recent Ball Events

* **Key**: `match:{match_id}:events`
* **Type**: `LIST`

**Notes**

* Stores the last **N** events (e.g., 100 balls)
* Trimmed using `LTRIM`

---

### 4.3 Active Subscribers

* **Key**: `match:{match_id}:subscribers`
* **Type**: `SET`

**Purpose**

* Tracks active WebSocket connections
* Used for analytics and cleanup

---

### 4.4 Pub/Sub Channel

* **Channel**: `match:{match_id}:channel`

**Published Events**

* `BALL_UPDATE`
* `WICKET`
* `MATCH_END`

---

## 5. TTL Strategy

| Key                      | TTL                       | Reason                        |
| ------------------------ | ------------------------- | ----------------------------- |
| `match:{id}:state`       | Until match ends + 1 hour | Serve late viewers            |
| `match:{id}:events`      | Same as state             | Maintain short history        |
| `match:{id}:subscribers` | No TTL                    | Managed on connect/disconnect |
| Pub/Sub channels         | N/A                       | Ephemeral                     |

**On match completion:**

* Keys are explicitly deleted **or**
* TTL is reduced to a short duration

---

## 6. Eviction Policy

**Redis Configuration**

```conf
maxmemory-policy allkeys-lru
```

**Reason**

* Live data is accessed most frequently
* Least Recently Used data is safe to evict

---

## 7. Atomicity & Consistency

* `HINCRBY` for score updates
* `MULTI / EXEC` for grouped updates
* Prevents partial or inconsistent state updates

---

## 8. Redis Pub/Sub Flow

1. Admin submits a match update
2. Redis match state is updated
3. Event is published to Redis channel
4. All backend instances receive the event
5. WebSocket servers broadcast to clients

---

## 9. Failure Handling

| Scenario             | Behavior                    |
| -------------------- | --------------------------- |
| Redis unavailable    | Fallback to database        |
| Pub/Sub message loss | Next update corrects state  |
| Instance crash       | No data loss (Redis shared) |

---

## 10. Rate Limiting (Redis-Based)

**Key Pattern**

```
rate:{user_id}:{endpoint}
```

**Logic**

* Incremented per request
* TTL = rate-limit window
* Exceeding limit → `HTTP 429 Too Many Requests`

---

## 11. Capacity Estimation (Preview)

| Item                | Estimate |
| ------------------- | -------- |
| Live matches        | 50       |
| Avg users per match | 20,000   |
| Keys per match      | ~5       |
| Total keys          | ~250     |
| Memory usage        | < 100 MB |

📄 Detailed analysis available in `capacity-estimation.md`

---

## 12. Security Considerations

* Redis is not publicly exposed
* Authenticated access only
* TLS enabled in production
* No sensitive data stored

---

## 13. Trade-offs

| Choice               | Reason                   |
| -------------------- | ------------------------ |
| Pub/Sub over Streams | Simpler, lower latency   |
| Cache over DB reads  | High performance         |
| TTL-based cleanup    | Predictable memory usage |

---

## 14. What This Enables

* Real-time fan-out at scale
* Minimal database load
* Stateless WebSocket servers
* Predictable memory utilization

---

