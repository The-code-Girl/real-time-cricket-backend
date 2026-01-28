# 🏏 Real-Time Cricket Match Platform

A **production-grade, backend-focused** real-time cricket live scoring and match management platform,
built to demonstrate **scalable system design**, **low-latency streaming**, and **clean backend architecture**.

The project follows a **design-first, industry-style development approach** commonly used in large engineering teams.

---

## ✨ Key Features

- 🏏 Live match scoring (runs, wickets, overs, ball-by-ball)
- ⚡ Real-time updates using WebSockets
- 👤 Role-based access control (Admin / User)
- 🧠 Redis-backed caching & pub/sub for high-throughput fan-out
- 🗃 Persistent match history in PostgreSQL
- 🧱 Clean layered architecture (API, Service, Domain, Infra)
- 🖥 Lightweight frontend to visualize real-time data

---

## 📐 System Design & Documentation

All major system design artifacts are documented in the `/docs` directory:

- `requirements.md` – Functional & non-functional requirements
- `hld.md` – High-Level Architecture
- `lld.md` – Low-Level Design (services, entities, flows)
- `api-contracts.md` – REST & WebSocket contracts
- `redis-design.md` – Caching, pub/sub, TTL & eviction strategy
- `capacity-estimation.md` – Traffic assumptions, sizing & scaling strategy

This mirrors **real-world design documentation** used in production systems.

---

## 🛠 Tech Stack

**Backend**
- FastAPI (Async REST APIs + WebSockets)
- Python 3.11+

**Data**
- PostgreSQL – source of truth
- Redis – caching, pub/sub, live match state

**Security**
- JWT-based authentication
- Role-based authorization

**Infra & Tooling**
- Docker & Docker-Compose
- Alembic (DB migrations)
- Swagger / OpenAPI
- Postman collections

---

## 🧩 Architecture Overview

- REST APIs for match lifecycle & admin operations
- WebSockets for real-time score broadcasting
- Redis Pub/Sub for horizontal scalability
- Stateless backend services
- PostgreSQL for durable match history

---

## 🖥 Minimal Frontend (WebSocket Demo)

A lightweight HTML + JavaScript frontend is included to visualize
real-time match updates via WebSockets.

Purpose:
- Validate end-to-end real-time flow
- Demonstrate Redis pub/sub + WebSocket fan-out
- Keep focus on backend architecture

No frontend framework is used intentionally.

---

## 🚧 Project Status

✔️ System design & architecture completed  
✔️ Backend APIs, authentication, Redis & WebSockets implemented  
🔨 Enhancements, testing & observability improvements in progress  

---

## 🎯 Why This Project?

This project is built to showcase:
- Real-time backend system design
- Distributed caching strategies
- API & WebSocket design
- Scalability & capacity planning
- Production-quality backend engineering practices
