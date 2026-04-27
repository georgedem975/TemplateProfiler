from fastapi import Depends
from ..depends import get_db
from ..schema.benchmark import BenchmarkRecordSchema, BenchmarkRecordCreateSchema


class BenchmarkService:
    def __init__(self, db):
        self.db = db

    async def get_benchmarks(self) -> list[BenchmarkRecordSchema]:
        benchmarks_record = await self.db.get_benchmarks()
        benchmarks_record = [BenchmarkRecordSchema.model_validate(benchmark) for benchmark in benchmarks_record]
        return benchmarks_record

    async def create_benchmark(self, benchmark: BenchmarkRecordCreateSchema) -> BenchmarkRecordSchema:
        db_benchmark = await self.db.insert_benchmark(
            template_engine=benchmark.template_engine,
            render_time_ms=benchmark.render_time_ms,
            payload=benchmark.payload,
        )
        db_benchmark = BenchmarkRecordSchema.model_validate(db_benchmark)
        return db_benchmark


def get_benchmark_service(db = Depends(get_db)) -> BenchmarkService:
    return BenchmarkService(db)
