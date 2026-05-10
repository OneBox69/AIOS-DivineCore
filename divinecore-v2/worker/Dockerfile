FROM python:3.12-slim

WORKDIR /app

# Build context is the repo root (set in docker-compose / CI).
COPY divinecore-v2/worker/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# worker source flattens into /app (so `celery -A celery_app` works as before)
COPY divinecore-v2/worker/ ./

# domain modules live at /app/<module>/, importable via `sales_os.integrations.upwork.processor` etc.
COPY sales_os/ ./sales_os/
COPY ops_os/ ./ops_os/

CMD ["celery", "-A", "celery_app", "worker", "--loglevel=info"]
