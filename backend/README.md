# Backend — SQLite Persistence

Async SQLite persistence layer for template benchmark records.

## Stack

- Python 3.11+
- aiosqlite

## Setup

```bash
pip install -r requirements.txt
```

## Database

SQLite file `benchmarks.db`, created automatically on first run.

Schema:

```sql
CREATE TABLE IF NOT EXISTS benchmarks (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    template_engine TEXT    NOT NULL,
    render_time_ms  TEXT    NOT NULL,
    payload         TEXT    NOT NULL,
    created_at      TEXT    NOT NULL DEFAULT (datetime('now'))
);
```

> `render_time_ms` — TEXT, чтобы сохранить формат `"2.000"`.

## API (db.py)

```python
await init_db()                                          # создать таблицу
await insert_benchmark(engine, render_time_ms, payload)  # сохранить запись
await get_benchmarks()                                   # получить все записи (новые первыми)
```

## Tests

```bash
pytest
```
