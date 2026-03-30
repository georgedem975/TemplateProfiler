from fastapi import APIRouter, Depends

from app.schema.benchmark import BenchmarkRecordCreateSchema, BenchmarkRecordSchema
from app.services.bechmark import BenchmarkService, get_benchmark_service

router = APIRouter(
    prefix="/benchmarks",
    tags=["benchmarks"],
)

@router.get("/")
async def get_benchmarks(service: BenchmarkService = Depends(get_benchmark_service)) -> list[BenchmarkRecordSchema]:
    benchmarks_record = await service.get_benchmarks()
    return benchmarks_record

@router.post("/")
async def create_benchmark(benchmark: BenchmarkRecordCreateSchema, service: BenchmarkService = Depends(get_benchmark_service)) -> BenchmarkRecordSchema:
    benchmarks_record = await service.create_benchmark(benchmark)
    return benchmarks_record