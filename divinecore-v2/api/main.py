from fastapi import FastAPI
from pydantic import BaseModel
from celery import Celery

from routes.fathom import router as fathom_router
from settings import settings

celery_client = Celery("api", broker=settings.REDIS_URL, backend=settings.REDIS_URL)

app = FastAPI(title="DivineCore v2")
app.include_router(fathom_router)


class EchoRequest(BaseModel):
    message: str


@app.get("/")
def root():
    return {"status": "ok", "service": "DivineCore v2 API"}


@app.post("/tasks/echo")
def trigger_echo(req: EchoRequest):
    result = celery_client.send_task("tasks.echo", args=[req.message])
    return {"task_id": result.id, "submitted": req.message}


@app.get("/tasks/{task_id}")
def get_task(task_id: str):
    result = celery_client.AsyncResult(task_id)
    return {
        "task_id": task_id,
        "status": result.status,
        "result": result.result if result.ready() else None,
    }
