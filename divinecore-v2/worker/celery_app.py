import os
from celery import Celery
from celery.schedules import crontab

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

app = Celery(
    "divinecore",
    broker=REDIS_URL,
    backend=REDIS_URL,
    include=[
        "tasks",
        "ops_os.integrations.fathom.processor",
        "ops_os.integrations.fathom.poller",
        "sales_os.integrations.upwork.processor",
        "sales_os.integrations.instantly.processor",
    ],
)

app.conf.beat_schedule = {
    "heartbeat-every-30s": {
        "task": "tasks.heartbeat",
        "schedule": 30.0,
    },
    "poll-fathom-every-10m": {
        "task": "tasks.poll_fathom_recordings",
        "schedule": 600.0,
    },
    "poll-instantly-campaigns-daily": {
        # 00:30 UTC every day. Snapshots yesterday's cumulative campaign
        # analytics from Instantly into outreach_daily_step_metrics.
        "task": "tasks.poll_instantly_campaigns",
        "schedule": crontab(hour=0, minute=30),
    },
}
