import logging

from fastapi import APIRouter, Depends

from ..schema.benchmark import BenchmarkRecordCreateSchema, BenchmarkRecordSchema
from ..services.benchmark import BenchmarkService, get_benchmark_service

router = APIRouter(
    prefix="/benchmarks",
    tags=["benchmarks"],
)

logger = logging.getLogger(__name__)

@router.get("/")
async def get_benchmarks(service: BenchmarkService = Depends(get_benchmark_service)) -> list[BenchmarkRecordSchema]:
    logger.info("get_benchmarks_started")
    benchmarks_record = await service.get_benchmarks()
    logger.info("get_benchmarks_succeeded count=%s", len(benchmarks_record))
    return benchmarks_record

@router.post("/")
async def create_benchmark(benchmark: BenchmarkRecordCreateSchema, service: BenchmarkService = Depends(get_benchmark_service)) -> BenchmarkRecordSchema:
    logger.info("create_benchmark_started engine=%s", benchmark.template_engine)
    benchmarks_record = await service.create_benchmark(benchmark)
    logger.info("create_benchmark_succeeded id=%s", benchmarks_record.id)
    return benchmarks_record