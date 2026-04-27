import pytest
from unittest.mock import AsyncMock, patch
from fastapi.testclient import TestClient


from app.schema.benchmark import BenchmarkRecordSchema, BenchmarkRecordCreateSchema
from app.services.benchmark import BenchmarkService
from main import app



@pytest.fixture
def client():
    """Создание тестового клиента"""
    return TestClient(app)


@pytest.fixture
def mock_db():
    """Mock для базы данных"""
    mock = AsyncMock()
    return mock


@pytest.fixture
def benchmark_service(mock_db):
    """Фикстура для сервиса с mock БД"""
    return BenchmarkService(mock_db)


@pytest.fixture
def sample_benchmark_data():
    """Пример данных для тестов"""
    return {
        "template_engine": "mustache",
        "render_time_ms": "1.234",
        "payload": '{"key": "value", "number": 42}'
    }


@pytest.fixture
def sample_benchmark_record(sample_benchmark_data):
    """Пример записи из БД"""
    return BenchmarkRecordSchema(
        id=1,
        created_at="2024-01-01T12:00:00",
        **sample_benchmark_data
    )



class TestBenchmarkRecordCreateSchema:
    """Тесты для схемы создания записи"""

    def test_valid_benchmark_record(self, sample_benchmark_data):
        """Тест валидных данных"""
        record = BenchmarkRecordCreateSchema(**sample_benchmark_data)
        assert record.template_engine == "mustache"
        assert record.render_time_ms == "1.234"
        assert record.payload == '{"key": "value", "number": 42}'

    def test_invalid_template_engine(self, sample_benchmark_data):
        """Тест невалидного template_engine"""
        sample_benchmark_data["template_engine"] = "invalid_engine"
        with pytest.raises(ValueError) as exc_info:
            BenchmarkRecordCreateSchema(**sample_benchmark_data)
        assert "template_engine must be one of" in str(exc_info.value)

    def test_all_allowed_template_engines(self, sample_benchmark_data):
        """Тест всех разрешенных template_engine"""
        allowed_engines = ['mustache', 'handlebars', 'lodash', 'ejs', 'nunjucks', 'eta']
        for engine in allowed_engines:
            sample_benchmark_data["template_engine"] = engine
            record = BenchmarkRecordCreateSchema(**sample_benchmark_data)
            assert record.template_engine == engine

    def test_invalid_render_time_ms_not_float(self, sample_benchmark_data):
        """Тест невалидного render_time_ms (не число)"""
        sample_benchmark_data["render_time_ms"] = "not_a_number"
        with pytest.raises(ValueError) as exc_info:
            BenchmarkRecordCreateSchema(**sample_benchmark_data)
        assert "render_time_ms must be an valid float" in str(exc_info.value)

    def test_render_time_ms_formatting(self, sample_benchmark_data):
        """Тест форматирования render_time_ms до 3 знаков"""
        sample_benchmark_data["render_time_ms"] = "1.234567"
        record = BenchmarkRecordCreateSchema(**sample_benchmark_data)
        assert record.render_time_ms == "1.235"

    def test_render_time_ms_int_conversion(self, sample_benchmark_data):
        """Тест конвертации целого числа"""
        sample_benchmark_data["render_time_ms"] = "5"
        record = BenchmarkRecordCreateSchema(**sample_benchmark_data)
        assert record.render_time_ms == "5.000"

    def test_invalid_payload(self, sample_benchmark_data):
        """Тест невалидного JSON в payload"""
        sample_benchmark_data["payload"] = "not a valid json"
        with pytest.raises(ValueError) as exc_info:
            BenchmarkRecordCreateSchema(**sample_benchmark_data)
        assert "payload must be valid JSON string" in str(exc_info.value)

    def test_valid_payload_various_json(self, sample_benchmark_data):
        """Тест валидных JSON различных форматов"""
        json_examples = [
            '{"key": "value"}',
            '{"numbers": [1, 2, 3]}',
            '{"nested": {"inner": "value"}}',
            '["array", "of", "strings"]',
            '"simple string"',
            'null',
            'true',
            '42'
        ]

        for json_str in json_examples:
            sample_benchmark_data["payload"] = json_str
            record = BenchmarkRecordCreateSchema(**sample_benchmark_data)
            assert record.payload == json_str


# ==================== Тесты для сервиса ====================

class TestBenchmarkService:
    """Тесты для BenchmarkService"""

    @pytest.mark.asyncio
    async def test_get_benchmarks(self, benchmark_service, mock_db, sample_benchmark_record):
        """Тест получения всех записей"""
        mock_db.get_benchmarks.return_value = [sample_benchmark_record.model_dump()]

        result = await benchmark_service.get_benchmarks()

        assert len(result) == 1
        assert result[0].id == sample_benchmark_record.id
        assert result[0].template_engine == sample_benchmark_record.template_engine
        mock_db.get_benchmarks.assert_called_once()

    @pytest.mark.asyncio
    async def test_get_benchmarks_empty(self, benchmark_service, mock_db):
        """Тест получения пустого списка"""
        mock_db.get_benchmarks.return_value = []

        result = await benchmark_service.get_benchmarks()

        assert result == []
        mock_db.get_benchmarks.assert_called_once()

    @pytest.mark.asyncio
    async def test_create_benchmark(self, benchmark_service, mock_db, sample_benchmark_data, sample_benchmark_record):
        """Тест создания записи"""
        mock_db.insert_benchmark.return_value = sample_benchmark_record.model_dump()

        create_schema = BenchmarkRecordCreateSchema(**sample_benchmark_data)
        result = await benchmark_service.create_benchmark(create_schema)

        assert result.id == sample_benchmark_record.id
        assert result.template_engine == sample_benchmark_record.template_engine
        assert result.render_time_ms == sample_benchmark_record.render_time_ms
        assert result.payload == sample_benchmark_record.payload

        mock_db.insert_benchmark.assert_called_once_with(
            template_engine=create_schema.template_engine,
            render_time_ms=create_schema.render_time_ms,
            payload=create_schema.payload
        )


# ==================== Тесты для эндпоинтов API ====================

class TestBenchmarkAPI:
    """Тесты API эндпоинтов"""

    def test_get_benchmarks_endpoint(self, client, sample_benchmark_record):
        """Тест GET /benchmarks/"""
        with patch('app.services.benchmark.BenchmarkService.get_benchmarks') as mock_get:
            mock_get.return_value = [sample_benchmark_record]

            response = client.get("/benchmarks/")

            assert response.status_code == 200
            data = response.json()
            assert len(data) == 1
            assert data[0]["id"] == sample_benchmark_record.id
            assert data[0]["template_engine"] == sample_benchmark_record.template_engine

    def test_get_benchmarks_endpoint_empty(self, client):
        """Тест GET /benchmarks/ когда нет записей"""
        with patch('app.services.benchmark.BenchmarkService.get_benchmarks') as mock_get:
            mock_get.return_value = []

            response = client.get("/benchmarks/")

            assert response.status_code == 200
            assert response.json() == []

    def test_create_benchmark_endpoint_valid(self, client, sample_benchmark_data, sample_benchmark_record):
        """Тест POST /benchmarks/ с валидными данными"""
        with patch('app.services.benchmark.BenchmarkService.create_benchmark') as mock_create:
            mock_create.return_value = sample_benchmark_record

            response = client.post("/benchmarks/", json=sample_benchmark_data)

            assert response.status_code == 200
            data = response.json()
            assert data["id"] == sample_benchmark_record.id
            assert data["template_engine"] == sample_benchmark_data["template_engine"]
            assert data["render_time_ms"] == sample_benchmark_data["render_time_ms"]
            assert data["payload"] == sample_benchmark_data["payload"]

            mock_create.assert_called_once()
            call_args = mock_create.call_args[0][0]
            assert call_args.template_engine == sample_benchmark_data["template_engine"]
            assert call_args.render_time_ms == sample_benchmark_data["render_time_ms"]
            assert call_args.payload == sample_benchmark_data["payload"]

    def test_create_benchmark_endpoint_invalid_template_engine(self, client, sample_benchmark_data):
        """Тест POST /benchmarks/ с невалидным template_engine"""
        sample_benchmark_data["template_engine"] = "invalid"

        response = client.post("/benchmarks/", json=sample_benchmark_data)

        assert response.status_code == 400
        assert "Validation errors:" in response.text
        assert "template_engine must be one of" in response.text

    def test_create_benchmark_endpoint_invalid_render_time(self, client, sample_benchmark_data):
        """Тест POST /benchmarks/ с невалидным render_time_ms"""
        sample_benchmark_data["render_time_ms"] = "not_a_number"

        response = client.post("/benchmarks/", json=sample_benchmark_data)

        assert response.status_code == 400
        assert "Validation errors:" in response.text
        assert "render_time_ms must be an valid float" in response.text

    def test_create_benchmark_endpoint_invalid_payload(self, client, sample_benchmark_data):
        """Тест POST /benchmarks/ с невалидным payload"""
        sample_benchmark_data["payload"] = "not a valid json"

        response = client.post("/benchmarks/", json=sample_benchmark_data)

        assert response.status_code == 400
        assert "Validation errors:" in response.text
        assert "payload must be valid JSON string" in response.text

    def test_create_benchmark_endpoint_missing_fields(self, client):
        """Тест POST /benchmarks/ с отсутствующими полями"""
        response = client.post("/benchmarks/", json={})

        assert response.status_code == 400
        assert "Validation errors:" in response.text