# Backend Service

## 📌 Overview

This is a simple monolithic web service responsible for storing and retrieving template rendering benchmark results.

The service exposes two HTTP endpoints:

* `POST /benchmarks` — store benchmark result
* `GET /benchmarks` — retrieve stored results

The goal is to keep the implementation minimal and focused, without overengineering (no strict layering).

---

## 🧠 Data Model

Each record contains:

* `template_engine` (string) — name of the templating engine
* `render_time_ms` (float) — rendering time in milliseconds
* `payload` (string/json) — optional input data used for rendering

---

## ⚙️ Tech Stack

* Python
* Flask (or similar lightweight framework)
* SQLite (default storage)

---

## 📡 API Contract

### POST /benchmarks

Store a benchmark result.

**Request body (JSON):**

```json
{
  "template_engine": "jinja2",
  "render_time_ms": 12.5,
  "payload": "{ \"data\": 123 }"
}
```

**Response:**

```json
{
  "status": "ok"
}
```

---

### GET /results

Retrieve stored results.

**Query params (optional):**

* `template_engine`

**Response:**

```json
[
  {
    "template_engine": "jinja2",
    "render_time_ms": 12.5,
    "payload": "..."
  }
]
```