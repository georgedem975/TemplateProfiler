"""Async SQLite persistence layer for benchmark records."""

import logging
from typing import TypedDict

import aiosqlite

DB_PATH = "benchmarks.db"
logger = logging.getLogger(__name__)


class BenchmarkRecord(TypedDict):
    id: int
    template_engine: str
    render_time_ms: str
    payload: str
    created_at: str


async def init_db() -> None:
    """Create the benchmarks table if it does not exist."""
    logger.info("db_init_started path=%s", DB_PATH)
    try:
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
        logger.info("db_init_succeeded")
    except Exception:
        logger.exception("db_init_failed")
        raise


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
    logger.info("db_insert_started engine=%s", template_engine)
    try:
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
    except Exception:
        logger.exception("db_insert_failed engine=%s", template_engine)
        raise

    logger.info("db_insert_succeeded id=%s", row_id)

    return BenchmarkRecord(
        id=row[0],
        template_engine=row[1],
        render_time_ms=row[2],
        payload=row[3],
        created_at=row[4],
    )


async def get_benchmarks() -> list[BenchmarkRecord]:
    """Return all benchmark records ordered from newest to oldest."""
    logger.info("db_get_benchmarks_started")
    try:
        async with aiosqlite.connect(DB_PATH) as db:
            async with db.execute(
                "SELECT id, template_engine, render_time_ms, payload, created_at"
                " FROM benchmarks ORDER BY id DESC"
            ) as cursor:
                rows = await cursor.fetchall()
    except Exception:
        logger.exception("db_get_benchmarks_failed")
        raise

    logger.info("db_get_benchmarks_succeeded count=%s", len(rows))

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
