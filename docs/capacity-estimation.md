📊 Capacity Estimation & Scaling Strategy — Cricket Live Platform
1. Purpose

This document estimates traffic, storage, memory, and compute needs for the Cricket Live Platform and defines a scaling strategy to handle peak loads during live matches.

2. Assumptions
Traffic Assumptions (Peak Event)

Concurrent live matches: 50

Average concurrent users per match: 20,000

Peak concurrent users total: 1,000,000

Admin scorers per match: 2

Match duration: 3 hours

3. Read & Write Patterns
3.1 Write Traffic (Admin Scoring)

Ball updates per over: 6

Overs per match: 50

Total balls per match: 300

Events per match: ~350 (including wickets, extras)

Writes per second (peak):

50 matches × 1 ball / 30 sec ≈ 1.6 writes/sec


➡️ Very low write traffic (easy to scale)

3.2 Read Traffic (Users)
REST API Reads

Initial match load per user

Assume 1 REST fetch per user

1,000,000 users / 10 minutes ≈ 1,666 RPS

WebSocket Messages

Every ball update broadcasted

50 matches × 1 update / 30 sec = ~1.6 events/sec


Each event fan-outs to:

20,000 users per match


➡️ WebSocket fan-out is the real load, not REST.

4. WebSocket Capacity
Concurrent Connections

Peak WebSocket connections: 1M

Backend Instance Capacity

Conservative estimate: 50,000 connections / instance

1,000,000 / 50,000 = 20 instances


➡️ Plan for 25 instances (buffer)

5. Redis Capacity Estimation
5.1 Key Count
Key Type	Per Match	Total
Live state	1	50
Event list	1	50
Subscribers	1	50
Rate limits	~10K	~500K
5.2 Memory Usage
Live State

~1 KB per match → 50 KB

Events

100 events × 300 bytes = 30 KB / match → 1.5 MB

Rate Limits

~100 bytes/key × 500K → 50 MB

➡️ Total Redis Memory ≈ 100 MB

Provision: 512 MB – 1 GB Redis instance

6. PostgreSQL Storage Estimation
Ball Events

Events per match: 350

Matches per day: 100

Events per day: 35,000

Yearly Storage
35,000 × 365 ≈ 12.7M rows

Row Size

~300 bytes / row

12.7M × 300B ≈ 3.8 GB / year


➡️ PostgreSQL easily handles this with indexing.

7. API Throughput
REST APIs

Peak: ~2K RPS

FastAPI can handle ~5–10K RPS per instance

➡️ 5–6 API instances sufficient

8. Scaling Strategy
8.1 Horizontal Scaling
Component	Strategy
API	Stateless, autoscale
WebSocket	Redis Pub/Sub
Redis	Primary + replica
DB	Read replicas
8.2 Autoscaling Triggers

CPU > 70%

Active WebSocket connections

Redis memory usage

API response latency

9. Fault Tolerance
Failure	Handling
API crash	Load balancer reroutes
WS server down	Client reconnect
Redis down	Read from DB
DB down	Read-only degraded mode
10. Cost Awareness (Rough)
Component	Estimate
API instances	Medium
Redis	Low
DB	Medium
Bandwidth	High (WebSockets)

➡️ WebSocket traffic is the dominant cost

11. Bottlenecks & Mitigation
Bottleneck	Mitigation
WS fan-out	Horizontal scale
Redis Pub/Sub	Sharding by match
DB writes	Async batching
Cold starts	Warm pools
12. Trade-offs
Decision	Reason
WebSockets	True real-time
Redis	Low latency
Eventual consistency	Performance
13. Final Summary

Write load is minimal

Read & fan-out dominate

Redis is critical

WebSockets define scale

Architecture supports 10× growth