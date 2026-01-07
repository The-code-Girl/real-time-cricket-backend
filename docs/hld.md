📐 High-Level Design (HLD) — Cricket Live Platform
1. Purpose

This document describes the high-level architecture of the Cricket Live Platform, focusing on:

Major system components

Data flow

Technology choices

Scalability and reliability considerations

It acts as a bridge between requirements and low-level design (LLD).

2. System Overview

The system is a real-time, event-driven backend platform where:

Admins publish live cricket match events

Users consume real-time updates via WebSockets

Redis acts as the real-time backbone

PostgreSQL stores durable match data

The architecture is stateless, horizontally scalable, and cloud-ready.

3. High-Level Architecture Diagram (Logical)
                ┌────────────┐
                │   Clients  │
                │ (Web/Mobile)│
                └─────┬──────┘
                      │
              ┌───────▼────────┐
              │ Load Balancer   │
              └───────┬────────┘
                      │
        ┌─────────────▼─────────────┐
        │     FastAPI Backend        │
        │ (REST + WebSocket APIs)    │
        └───────┬─────────┬─────────┘
                │         │
        ┌───────▼───┐ ┌──▼────────┐
        │ PostgreSQL │ │   Redis   │
        │ (History)  │ │ Cache +   │
        │             │ │ Pub/Sub  │
        └────────────┘ └───────────┘

4. Core Components
4.1 API Gateway / Backend Service (FastAPI)

Responsibilities:

Handle REST APIs (auth, match management, history)

Manage WebSocket connections

Validate JWT tokens

Enforce role-based access control

Publish/consume Redis events

Why FastAPI

Async-first (important for WebSockets)

High performance

Clean dependency injection

Auto API documentation

4.2 WebSocket Manager

Responsibilities:

Maintain active WebSocket connections

Map users to matches

Broadcast live updates to subscribers

Handle reconnects gracefully

Key Characteristics:

Stateless

Scales horizontally

Uses Redis Pub/Sub for cross-instance messaging

4.3 Redis

Used for:

Live match state caching

Pub/Sub for real-time updates

Temporary data (TTL-based)

Why Redis

Extremely low latency

Native Pub/Sub

Shared state across instances

Reduces database load

4.4 PostgreSQL

Responsibilities:

Persistent storage of:

Matches

Teams

Players

Ball-by-ball history

Source of truth for completed matches

Design Choice:

Strong consistency

ACID compliance

Mature indexing & migration support

4.5 Authentication & Authorization

JWT-based authentication

Role-based access:

ADMIN

USER

Middleware-based enforcement

5. Data Flow
5.1 Live Match Update Flow (Admin → Users)

Admin sends ball update via REST API

Backend validates:

JWT

Admin role

Update written to Redis (live state)

Event published to Redis Pub/Sub

All WebSocket servers receive event

Update broadcasted to subscribed users

Periodic persistence to PostgreSQL

5.2 User Subscription Flow

User connects to WebSocket

JWT validated

User subscribes to match channel

Initial state fetched from Redis

Continuous updates streamed in real time

5.3 Match Completion Flow

Admin marks match as completed

Final state persisted to PostgreSQL

Redis cache invalidated (or TTL expiry)

WebSocket channel closed gracefully

6. Scalability Strategy
6.1 Horizontal Scaling

Backend instances are stateless

WebSockets scale via Redis Pub/Sub

Load balancer distributes traffic

6.2 Read Optimization

Live reads served from Redis

Historical reads served from PostgreSQL

DB protected from read spikes

6.3 Write Optimization

Admin writes are low volume

Writes are validated and serialized

Batched DB writes (optional)

7. Fault Tolerance
Component	Strategy
Backend	Multiple instances
Redis	Persistence + replication
PostgreSQL	Backups + failover
WebSockets	Reconnect support
8. Security Considerations

HTTPS only

Secure WebSocket (wss)

JWT expiry & refresh strategy

Rate limiting on REST APIs

Input validation everywhere

9. Deployment Overview

Dockerized services

Docker Compose (local)

Kubernetes-ready architecture

Environment-based config

10. Trade-offs & Decisions
Decision	Reason
Redis Pub/Sub	Simplicity + speed
PostgreSQL	Strong consistency
FastAPI	Async performance
Stateless services	Easy scaling
11. What This Enables

This HLD enables:

Clean LLD

Clear API contracts

Confident capacity estimation

Interview-ready system explanation

git add docs/hld.md
git commit -m "Add high level system design (HLD)"
git push
