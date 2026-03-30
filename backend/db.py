import aiosqlite

DB_PATH = "benchmarks.db"


async def init_db() -> None:
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


async def insert_benchmark(template_engine: str, render_time_ms: str, payload: str) -> dict:
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute(
            "INSERT INTO benchmarks (template_engine, render_time_ms, payload) VALUES (?, ?, ?)",
            (template_engine, render_time_ms, payload),
        )
        await db.commit()
        row_id = cursor.lastrowid

    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute(
            "SELECT id, template_engine, render_time_ms, payload, created_at FROM benchmarks WHERE id = ?",
            (row_id,),
        ) as cur:
            row = await cur.fetchone()

    return {
        "id": row[0],
        "template_engine": row[1],
        "render_time_ms": row[2],
        "payload": row[3],
        "created_at": row[4],
    }


async def get_benchmarks() -> list:
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute(
            "SELECT id, template_engine, render_time_ms, payload, created_at FROM benchmarks ORDER BY id DESC"
        ) as cursor:
            rows = await cursor.fetchall()

    return [
        {
            "id": row[0],
            "template_engine": row[1],
            "render_time_ms": row[2],
            "payload": row[3],
            "created_at": row[4],
        }
        for row in rows
    ]
