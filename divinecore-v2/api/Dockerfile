FROM python:3.12-slim

WORKDIR /app

# Build context is the repo root (set in docker-compose / CI).
COPY divinecore-v2/api/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# api source flattens into /app (so `uvicorn main:app` works as before)
COPY divinecore-v2/api/ ./

# domain modules live at /app/<module>/, importable via `from sales_os.web import ...`
COPY sales_os/ ./sales_os/
COPY branding_os/ ./branding_os/

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
