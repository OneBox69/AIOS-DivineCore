from datetime import datetime
from celery_app import app


@app.task(name="tasks.echo")
def echo(message: str) -> str:
    result = message.upper()
    print(f"[echo] {message} -> {result}", flush=True)
    return result


@app.task(name="tasks.heartbeat")
def heartbeat() -> str:
    now = datetime.utcnow().isoformat()
    print(f"[heartbeat] {now}", flush=True)
    return now
