🚀 Redis Design — Cricket Live Platform
1. Purpose

This document defines how Redis is used in the Cricket Live Platform for:

Live match state caching

Real-time pub/sub messaging

Reducing database load

Enabling horizontal scalability

2. Why Redis?

Redis is chosen because it provides:

Sub-millisecond latency

In-memory data access

Native Pub/Sub support

Atomic operations

TTL-based eviction

Redis acts as the real-time backbone of the system.

3. Redis Use Cases
Use Case	Description
Live State Cache	Current score, overs, wickets
Pub/Sub	Broadcast live events
Temporary Data	Active subscriptions
Rate Limiting	Request throttling
4. Redis Key Design
4.1 Live Match State
Key: match:{match_id}:state
Type: HASH


Fields

runs
wickets
overs
last_updated

4.2 Recent Ball Events
Key: match:{match_id}:events
Type: LIST


Stores last N events (e.g., 100)

Trimmed using LTRIM

4.3 Active Subscribers
Key: match:{match_id}:subscribers
Type: SET


Tracks active WebSocket users

Helps analytics and cleanup

4.4 Pub/Sub Channel
Channel: match:{match_id}:channel


Broadcasts:

BALL_UPDATE

WICKET

MATCH_END

5. TTL Strategy
Key	TTL	Reason
match:{id}:state	Until match ends + 1 hr	Serve late viewers
match:{id}:events	Same as state	History buffer
match:{id}:subscribers	No TTL	Managed on connect/disconnect
Pub/Sub	N/A	Ephemeral

On match completion:

Keys are explicitly deleted OR

TTL reduced to short duration

6. Eviction Policy
Redis Configuration
maxmemory-policy allkeys-lru


Reason

Live data is most frequently accessed

Least recently used data is safe to evict

7. Atomicity & Consistency

HINCRBY used for score updates

MULTI/EXEC for grouped updates

Prevents partial updates

8. Redis Pub/Sub Flow

Admin update received

Redis state updated

Event published to channel

All backend instances receive event

WebSocket servers broadcast

9. Failure Handling
Scenario	Behavior
Redis down	Fallback to DB
Pub/Sub message loss	Next update corrects state
Instance crash	No data loss
10. Rate Limiting (Redis-based)

Key

rate:{user_id}:{endpoint}


Incremented per request

TTL = window size

Exceed → HTTP 429

11. Capacity Estimation (Preview)
Item	Estimate
Live matches	50
Avg users/match	20K
Keys/match	~5
Total keys	~250
Memory	< 100 MB

Detailed estimation in capacity-estimation.md

12. Security Considerations

Redis not publicly exposed

Authenticated access only

TLS in production

No sensitive data stored

13. Trade-offs
Choice	Reason
Pub/Sub over Streams	Simpler, lower latency
Cache over DB reads	Performance
TTL-based cleanup	Predictable memory
14. What This Enables

Real-time fan-out at scale

Minimal DB load

Stateless WebSocket servers

Predictable memory usage