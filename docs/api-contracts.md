# 📡 API Contracts — Cricket Live Platform

## 1. Overview

This document defines the **REST** and **WebSocket** API contracts for the **Cricket Live Platform**.

* Follows RESTful principles
* Uses consistent request/response formats
* Designed for scalability and frontend independence

---

## 2. Common Standards

### 2.1 Base URL

```
/api/v1
```

---

### 2.2 Authentication

* **JWT-based authentication**
* Token must be sent in request headers:

```
Authorization: Bearer <JWT_TOKEN>
```

---

### 2.3 Standard Response Format

#### ✅ Success Response

```json
{
  "success": true,
  "data": {}
}
```

#### ❌ Error Response

```json
{
  "success": false,
  "error": {
    "code": "UNAUTHORIZED",
    "message": "Invalid or expired token"
  }
}
```

---

### 2.4 HTTP Status Codes

| Code | Meaning               |
| ---: | --------------------- |
|  200 | OK                    |
|  201 | Created               |
|  400 | Bad Request           |
|  401 | Unauthorized          |
|  403 | Forbidden             |
|  404 | Not Found             |
|  429 | Too Many Requests     |
|  500 | Internal Server Error |

---

## 3. Authentication APIs

### 3.1 Login

**POST** `/auth/login`

#### Request

```json
{
  "email": "admin@cricket.com",
  "password": "password123"
}
```

#### Response

```json
{
  "success": true,
  "data": {
    "access_token": "jwt-token",
    "expires_in": 3600,
    "role": "ADMIN"
  }
}
```

---

## 4. Match Management APIs (Admin Only)

### 4.1 Create Match

**POST** `/matches`

#### Request

```json
{
  "team_a": "India",
  "team_b": "Australia",
  "venue": "Wankhede",
  "overs": 20
}
```

#### Response

```json
{
  "success": true,
  "data": {
    "match_id": "uuid",
    "status": "SCHEDULED"
  }
}
```

---

### 4.2 Start Match

**POST** `/matches/{match_id}/start`

#### Response

```json
{
  "success": true,
  "data": {
    "status": "LIVE"
  }
}
```

---

### 4.3 Complete Match

**POST** `/matches/{match_id}/complete`

#### Response

```json
{
  "success": true,
  "data": {
    "status": "COMPLETED"
  }
}
```

---

## 5. Live Scoring APIs (Admin Only)

### 5.1 Add Ball Event

**POST** `/matches/{match_id}/ball`

#### Request

```json
{
  "over": 10,
  "ball": 3,
  "runs": 4,
  "extras": 0,
  "wicket": false
}
```

#### Response

```json
{
  "success": true,
  "data": {
    "current_score": "120/4",
    "overs": "10.3"
  }
}
```

---

### 5.2 Add Wicket Event

**POST** `/matches/{match_id}/wicket`

#### Request

```json
{
  "over": 12,
  "ball": 1,
  "dismissal_type": "bowled"
}
```

---

## 6. User Read APIs

### 6.1 Get Live Match State

**GET** `/matches/{match_id}/live`

#### Response

```json
{
  "success": true,
  "data": {
    "runs": 145,
    "wickets": 6,
    "overs": "18.3"
  }
}
```

---

### 6.2 Get Match History

**GET** `/matches/{match_id}`

#### Response

```json
{
  "success": true,
  "data": {
    "teams": "India vs Australia",
    "final_score": "182/7",
    "result": "India won by 12 runs"
  }
}
```

---

## 7. WebSocket API

### 7.1 Connection

```
ws://<host>/api/v1/ws?token=<JWT>
```

---

### 7.2 Subscribe to Match

**Client → Server**

```json
{
  "action": "SUBSCRIBE",
  "match_id": "uuid"
}
```

---

### 7.3 Live Update Message

**Server → Client**

```json
{
  "event": "BALL_UPDATE",
  "data": {
    "over": 10,
    "ball": 3,
    "runs": 4,
    "current_score": "120/4"
  }
}
```

---

### 7.4 Unsubscribe

```json
{
  "action": "UNSUBSCRIBE",
  "match_id": "uuid"
}
```

---

## 8. Error Handling

### 8.1 WebSocket Error

```json
{
  "event": "ERROR",
  "message": "Unauthorized subscription"
}
```

---

## 9. Versioning Strategy

* API versioned via URL (`/v1`)
* Breaking changes require a new version
* Backward compatibility is preserved

---

## 10. Rate Limiting (Preview)

| Endpoint      | Limit     |
| ------------- | --------- |
| Login         | 5 / min   |
| Admin scoring | 60 / min  |
| User reads    | 300 / min |

---

## 11. What This Enables

* 🚀 Frontend integration without backend changes
* 🧱 Stable APIs as the system grows
* 🧪 Easy API testing & mocking
* 📄 Clean OpenAPI / Swagger generation

---
