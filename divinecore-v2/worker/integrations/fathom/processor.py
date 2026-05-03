from celery_app import app

from . import airtable_writer, categorizer, pulse_bridge


@app.task(name="tasks.process_fathom_recording")
def process_fathom_recording(payload: dict) -> dict:
    category = categorizer.classify(payload)
    meeting_record = airtable_writer.upsert(payload, category)
    pulse_tasks = pulse_bridge.create_tasks_for_opted_in(payload, meeting_record)
    return {
        "meeting_id": payload.get("recording_id") or payload.get("id"),
        "category": category,
        "airtable_record_id": meeting_record.get("id"),
        "pulse_tasks_created": len(pulse_tasks),
    }
