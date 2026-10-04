# Document Search Service

Сервис полнотекстового поиска и удаления документов.

## Стек

- Python 3.12
- FastAPI
- PostgreSQL
- Elasticsearch
- SQLAlchemy
- Alembic
- Docker Compose

## Запуск

1. Создать `.env` из шаблона:

```powershell
Copy-Item .env.example .env
```

2. Запустить сервис:

```powershell
docker compose up --build
```

## Тесты

После запуска контейнеров тесты выполняются командой:

```powershell
docker compose exec app pytest
```

При первом запуске сервис автоматически:

- применит миграции Alembic;
- загрузит документы из `data/posts.csv` в PostgreSQL;
- создаст индекс Elasticsearch и заполнит его документами;
- запустит API на порту `8000`.

После запуска документация Swagger доступна по адресу:

```text
http://localhost:8000/docs
```

## Методы API

### Поиск документов

```http
GET /documents?query={query}
```

Выполняет поиск по полю `text` через Elasticsearch. Возвращает до 20 документов с полями `id`, `rubrics`, `text`, `created_date`.

Сначала Elasticsearch выбирает до 20 наиболее релевантных документов, затем результат сортируется по `created_date` в порядке убывания.

Пример:

```text
http://localhost:8000/documents?query=автомобиль
```

### Удаление документа

```http
DELETE /documents/{id}
```

Удаляет документ из PostgreSQL и Elasticsearch по идентификатору.

Успешный ответ: `204 No Content`.

Если документ не найден: `404 Not Found`.

## OpenAPI

Статическая OpenAPI-схема находится в файле `docs.json`.

## Повторный запуск

При повторном запуске CSV не импортируется повторно, если в таблице уже есть документы. Индекс Elasticsearch заполняется документами из PostgreSQL.