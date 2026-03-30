"""Async SQLite persistence layer for benchmark records."""

from typing import TypedDict

import aiosqlite

DB_PATH = "benchmarks.db"


class BenchmarkRecord(TypedDict):
    id: int
    template_engine: str
    render_time_ms: str
    payload: str
    created_at: str


async def init_db() -> None:
    """Create the benchmarks table if it does not exist."""
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS benchmarks (
                id              INTEGER PRIMARY KEY AUTOINCREMENT,
                template_engine TEXT    NOT NULL,
                render_time_ms  TEXT    NOT NULL,
                payload         TEXT    NOT NULL,
                created_at      TEXT    NOT NULL DEFAULT (datetime('now'))
            )
        """)
        await db.commit()


async def insert_benchmark(
    template_engine: str,
    render_time_ms: str,
    payload: str,
) -> BenchmarkRecord:
    """Insert a benchmark record and return the saved row.

    Args:
        template_engine: Name of the template engine (e.g. "mustache").
        render_time_ms:  Render time as a formatted string (e.g. "2.000").
                         Stored as TEXT to preserve trailing zeros.
        payload:         JSON string with the data used during rendering.

    Returns:
        The newly created record including auto-generated id and created_at.
    """
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute(
            "INSERT INTO benchmarks (template_engine, render_time_ms, payload) VALUES (?, ?, ?)",
            (template_engine, render_time_ms, payload),
        )
        await db.commit()
        row_id = cursor.lastrowid

    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute(
            "SELECT id, template_engine, render_time_ms, payload, created_at"
            " FROM benchmarks WHERE id = ?",
            (row_id,),
        ) as cur:
            row = await cur.fetchone()

    return BenchmarkRecord(
        id=row[0],
        template_engine=row[1],
        render_time_ms=row[2],
        payload=row[3],
        created_at=row[4],
    )


async def get_benchmarks() -> list[BenchmarkRecord]:
    """Return all benchmark records ordered from newest to oldest."""
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute(
            "SELECT id, template_engine, render_time_ms, payload, created_at"
            " FROM benchmarks ORDER BY id DESC"
        ) as cursor:
            rows = await cursor.fetchall()

    return [
        BenchmarkRecord(
            id=row[0],
            template_engine=row[1],
            render_time_ms=row[2],
            payload=row[3],
            created_at=row[4],
        )
        for row in rows
    ]
