import os
from celery import Celery

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

app = Celery(
    "divinecore",
    broker=REDIS_URL,
    backend=REDIS_URL,
    include=["tasks", "integrations.fathom.processor"],
)

app.conf.beat_schedule = {
    "heartbeat-every-30s": {
        "task": "tasks.heartbeat",
        "schedule": 30.0,
    },
}
