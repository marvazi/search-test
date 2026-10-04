
#!/bin/sh
set -e

alembic upgrade head
python -m scripts.import_csv
python -m scripts.index_documents

exec uvicorn app.main:app --host 0.0.0.0 --port 8000