Project: Template Benchmark Backend

Goal:
Build a minimal Flask-based backend service for storing and retrieving template rendering benchmark results.

Constraints:
- Keep architecture simple (monolith, no heavy layering)
- Use SQLite for persistence
- Provide clean and minimal API

Endpoints:
- POST /benchmarks
- GET /benchmarks

Data Model:
(template_engine: string, render_time_ms: float, payload: string/json)

Priorities:
- Simplicity
- Readability
- Fast implementation

Avoid:
- Overengineering
- Complex abstractions