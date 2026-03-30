import json

from fastapi import HTTPException
from pydantic import ValidationError

import db
from app.schema.benchmark import BenchmarkRecordSchema, BenchmarkRecordCreateSchema


class BenchmarkService:
    async def get_benchmarks(self) -> list[BenchmarkRecordSchema]:
        benchmarks_record = await db.get_benchmarks()
        try:
            benchmarks_record = [BenchmarkRecordSchema.model_validate(benchmark) for benchmark in benchmarks_record]
            return benchmarks_record
        except ValidationError as e:
            raise HTTPException(status_code=400, detail=json.loads(e.json()))

    async def create_benchmark(self, benchmark: BenchmarkRecordCreateSchema) -> BenchmarkRecordSchema:
        try:
            db_benchmark = await db.insert_benchmark(
                template_engine=benchmark.template_engine,
                render_time_ms=benchmark.render_time_ms,
                payload=benchmark.payload,
            )
            db_benchmark = BenchmarkRecordSchema.model_validate(db_benchmark)
            return db_benchmark
        except ValidationError as e:
            raise HTTPException(status_code=400, detail=json.loads(e.json()))

def get_benchmark_service() -> BenchmarkService:
    return BenchmarkService()