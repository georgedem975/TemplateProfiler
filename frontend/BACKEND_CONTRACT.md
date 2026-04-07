# Backend API Contract

Документ описывает что именно фронтенд отправляет и ожидает получить от бэкенда.
Реализовывать бэкенд нужно строго по этому документу — UI переделываться не будет.

---

## Base URL

```
http://localhost:5000
```

Vite dev-сервер проксирует все запросы `/benchmarks` → `http://localhost:5000`.
Прямые запросы с браузера идут на `http://localhost:5173`.

---

## CORS

Бэкенд обязан принимать запросы с origin `http://localhost:5173`.
Минимальные заголовки:

```
Access-Control-Allow-Origin: http://localhost:5173
Access-Control-Allow-Methods: GET, POST, OPTIONS
Access-Control-Allow-Headers: Content-Type
```

---

## Endpoints

### POST /benchmarks

Сохранить результат одного замера.

**Request**

```
Content-Type: application/json
```

```json
{
  "template_engine": "mustache",
  "render_time_ms": "2.000",
  "payload": "{\"name\": \"Alice\", \"count\": 5, \"admin\": true}"
}
```

| Поле | Тип | Описание |
|------|-----|----------|
| `template_engine` | string | Один из: `"mustache"`, `"handlebars"`, `"lodash"`, `"ejs"`, `"nunjucks"`, `"eta"` |
| `render_time_ms` | **string** | Время рендера в мс, всегда 3 знака после запятой. Пример: `"2.000"`, `"0.031"`. Хранить как TEXT/VARCHAR, не FLOAT — иначе `"2.000"` превратится в `2` |
| `payload` | string | JSON-объект с данными, использованными при рендере, сериализованный в строку |

**Response**

Любой 2xx статус. Фронтенд не использует тело ответа POST, но ожидает валидный JSON.
Рекомендуется `201 Created`:

```json
{
  "id": 1,
  "template_engine": "mustache",
  "render_time_ms": "2.000",
  "payload": "{\"name\": \"Alice\", \"count\": 5, \"admin\": true}",
  "created_at": "2026-03-29T10:00:00"
}
```

---

### GET /benchmarks

Получить все сохранённые результаты.

**Request** — без тела, без параметров.

**Response** `200 OK`

Массив объектов. Порядок — от новых к старым (или по `id` desc).

```json
[
  {
    "id": 1,
    "template_engine": "mustache",
    "render_time_ms": "2.000",
    "payload": "{\"name\": \"Alice\", \"count\": 5, \"admin\": true}",
    "created_at": "2026-03-29T10:00:00"
  },
  {
    "id": 2,
    "template_engine": "ejs",
    "render_time_ms": "1.400",
    "payload": "{\"name\": \"Alice\", \"count\": 5, \"admin\": true}",
    "created_at": "2026-03-29T10:01:00"
  }
]
```

| Поле | Тип | Описание |
|------|-----|----------|
| `id` | number | Уникальный идентификатор записи |
| `template_engine` | string | Название движка |
| `render_time_ms` | string | Время рендера — возвращать точно так же как пришло, строкой с 3 знаками |
| `payload` | string | JSON данных в виде строки |
| `created_at` | string | Дата и время сохранения, ISO 8601. Пример: `"2026-03-29T10:00:00"` |

---

## Хранение данных (SQLite)

Рекомендуемая схема таблицы:

```sql
CREATE TABLE benchmarks (
  id              INTEGER PRIMARY KEY AUTOINCREMENT,
  template_engine TEXT    NOT NULL,
  render_time_ms  TEXT    NOT NULL,
  payload         TEXT    NOT NULL,
  created_at      TEXT    NOT NULL DEFAULT (datetime('now'))
);
```

> `render_time_ms` — TEXT, не REAL/FLOAT, чтобы сохранить формат `"2.000"`.

---

## Обработка ошибок

Фронтенд показывает сообщение об ошибке при любом не-2xx ответе.
Специфический формат тела ошибки не требуется.
