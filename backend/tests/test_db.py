import os

import aiosqlite
import pytest

import db as db_module
from db import get_benchmarks, init_db, insert_benchmark

TEST_DB = "test_benchmarks.db"


@pytest.fixture(autouse=True)
def use_test_db(monkeypatch, tmp_path):
    test_path = str(tmp_path / "test.db")
    monkeypatch.setattr(db_module, "DB_PATH", test_path)
    yield


async def test_init_db_creates_table():
    await init_db()
    async with aiosqlite.connect(db_module.DB_PATH) as db:
        async with db.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='benchmarks'"
        ) as cur:
            row = await cur.fetchone()
    assert row is not None


async def test_insert_returns_record():
    await init_db()
    record = await insert_benchmark("mustache", "2.000", '{"name": "Alice"}')

    assert record["id"] == 1
    assert record["template_engine"] == "mustache"
    assert record["render_time_ms"] == "2.000"
    assert record["payload"] == '{"name": "Alice"}'
    assert "created_at" in record


async def test_render_time_stored_as_text():
    await init_db()
    await insert_benchmark("ejs", "2.000", "{}")
    records = await get_benchmarks()

    assert records[0]["render_time_ms"] == "2.000"


async def test_get_benchmarks_returns_newest_first():
    await init_db()
    await insert_benchmark("jinja2", "1.000", "{}")
    await insert_benchmark("ejs", "3.000", "{}")
    records = await get_benchmarks()

    assert len(records) == 2
    assert records[0]["template_engine"] == "ejs"
    assert records[1]["template_engine"] == "jinja2"


async def test_get_benchmarks_empty():
    await init_db()
    records = await get_benchmarks()
    assert records == []
