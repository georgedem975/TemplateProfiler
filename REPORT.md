# Результаты работы команды

## Отчёт по задачам и замеры производительности

## Состав команды и выполненные задачи

| Имя и фамилия | Роль | Telegram | Выполненные задачи | Ссылки на задачи |
|--------------|------|----------|------------------|----------------|
| Преображенский Георгий | Manager | [@georgedemyan](https://t.me/georgedemyan) | Организовал спринт, провёл планирование, координировал команду | [Documentation: maintain wiki and prepare release notes](https://github.com/georgedem975/TemplateProfiler/issues/7) |
| Костык Евгений | DevOps | [@jenyacpypy](https://t.me/jenyacpypy) | Настроил пайплайн непрерывной интеграции (CI) с помощью GitHub Actions | [DevOps: add CI pipeline to run unit tests](https://github.com/georgedem975/TemplateProfiler/issues/4) |
| Погоренко Иван | DevOps | [@Duduvvka](https://t.me/Duduvvka) | Развернул backend и frontend, а также базу данных на Render | [DevOps: deploy backend service to Render](https://github.com/georgedem975/TemplateProfiler/issues/3), [Deploy frontend service to Render](https://github.com/georgedem975/TemplateProfiler/issues/15) |
| Симаков Евгений | Frontend Разработчик | [@EvgeniiSimakov](https://t.me/EvgeniiSimakov) | Реализовал веб‑интерфейс сервиса | — |
| Савельева Диана | Backend Разработчик | [@di_svlv](https://t.me/di_svlv) | Реализовала уровень доступа к данным | [Backend: add SQLite persistence for benchmarks](https://github.com/georgedem975/TemplateProfiler/issues/1) |
| Пяигорец Александр | Backend Разработчик | [@jojiiikol](https://t.me/jojiiikol) | Реализовал HTTP‑API на Flask с эндпоинтами | [Backend: implement /benchmarks API endpoints](https://github.com/georgedem975/TemplateProfiler/issues/2) |
| Чирков Лев | Backend Разработчик | [@L1ones](https://t.me/L1ones) | Настроил логирование в бэкенд‑сервисе | [Backend: add structured logging](https://github.com/georgedem975/TemplateProfiler/issues/5) |
| Ангел Кантор Флорес | Тестировщик | [@Angel36b](https://t.me/Angel36b) | Написал тесты для CI, протестировал корректность работы развёрнутого программного обеспечения | [Frontend: write unit tests and test the deployed application](https://github.com/georgedem975/TemplateProfiler/issues/16) |

## Результаты замеров производительности

1. **Шаблонизатор Mustache** — время рендеринга: 2.200 мс.
2. **Шаблонизатор Handlebars** — время рендеринга: 13.300 мс.
3. **Шаблонизатор Lodash (_.template)** — время рендеринга: 8.500 мс.
4. **Шаблонизатор EJS** — время рендеринга: 13.300 мс.
5. **Шаблонизатор Nunjucks** — время рендеринга: 16.300 мс.
6. **Шаблонизатор Eta** — время рендеринга: 6.100 мс.

---

**Отчёт сформирован:** 28 апреля 2024 года
