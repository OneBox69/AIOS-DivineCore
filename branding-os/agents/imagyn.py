import os
import json
import httpx
import psycopg2
from psycopg2.extras import RealDictCursor
from datetime import datetime, timezone
from fastapi import APIRouter
from pydantic import BaseModel
from openai import OpenAI

router = APIRouter()
openai = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

SYSTEM_PROMPT = open(os.path.join(os.path.dirname(__file__), "IMAGYN_system_prompt.md")).read()
IMAGYN_BOT_ID = "1496791428020572230"
SESSION_KEY = "imagyn_global_memory"
MEMORY_LIMIT = 15

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "search_knowledge_base",
            "description": (
                "Search the Kallaway Core Knowledge Base. "
                "Call this before asking clarifying questions and before generating any ideas. "
                "Filter by one or more categories."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "categories": {
                        "type": "array",
                        "items": {
                            "type": "string",
                            "enum": ["Hook", "Format", "Emotion"]
                        },
                        "description": (
                            "Categories to fetch. "
                            "Use ['Format', 'Emotion'] when starting a conversation. "
                            "Add 'Hook' when the angle and feeling are agreed and you need to craft the title/opening."
                        )
                    }
                },
                "required": ["categories"]
            }
        }
    }
]


class DiscordPayload(BaseModel):
    username: str
    message: str
    author_id: str
    channel_id: str
    message_id: str


def db():
    return psycopg2.connect(os.getenv("SUPABASE_DB_URL"))


def load_history(conn, limit: int = MEMORY_LIMIT) -> list[dict]:
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute("""
            SELECT role, content FROM imagyn_messages
            WHERE session_id = %s
            ORDER BY created_at DESC
            LIMIT %s
        """, (SESSION_KEY, limit))
        rows = cur.fetchall()
    return [{"role": r["role"], "content": r["content"]} for r in reversed(rows)]


def save_turn(conn, user_content: str, assistant_content: str):
    now = datetime.now(timezone.utc)
    with conn.cursor() as cur:
        cur.execute(
            "INSERT INTO imagyn_messages (session_id, role, content, created_at) VALUES (%s, %s, %s, %s)",
            (SESSION_KEY, "user", user_content, now)
        )
        cur.execute(
            "INSERT INTO imagyn_messages (session_id, role, content, created_at) VALUES (%s, %s, %s, %s)",
            (SESSION_KEY, "assistant", assistant_content, now)
        )
    conn.commit()


def search_knowledge_base(categories: list[str]) -> list[dict]:
    conn = db()
    placeholders = ",".join(["%s"] * len(categories))
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute(
            f"SELECT title, category, core_lesson, full_explanation FROM branding_kb WHERE category IN ({placeholders})",
            tuple(categories)
        )
        results = [dict(r) for r in cur.fetchall()]
    conn.close()
    return results


async def send_discord_reply(channel_id: str, content: str, reply_to_id: str):
    token = os.getenv("IMAGYN_BOT_TOKEN")
    async with httpx.AsyncClient() as client:
        await client.post(
            f"https://discord.com/api/v10/channels/{channel_id}/messages",
            headers={"Authorization": f"Bot {token}"},
            json={
                "content": content,
                "message_reference": {"message_id": reply_to_id}
            }
        )


@router.post("/imagyn")
async def imagyn(payload: DiscordPayload):
    message = payload.message.replace(f"<@{IMAGYN_BOT_ID}>", "IMAGYN").strip()

    conn = db()
    history = load_history(conn)
    messages = history + [{"role": "user", "content": f"{payload.username}: {message}"}]

    # Agentic loop — runs until model stops calling tools
    while True:
        response = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "system", "content": SYSTEM_PROMPT}] + messages,
            tools=TOOLS,
            tool_choice="auto"
        )

        choice = response.choices[0].message

        if not choice.tool_calls:
            reply = choice.content
            save_turn(conn, f"{payload.username}: {message}", reply)
            conn.close()
            await send_discord_reply(payload.channel_id, reply, payload.message_id)
            return {"status": "ok"}

        # Execute each tool call and feed results back
        messages.append(choice)
        for tc in choice.tool_calls:
            args = json.loads(tc.function.arguments)
            results = search_knowledge_base(args["categories"])
            messages.append({
                "role": "tool",
                "tool_call_id": tc.id,
                "content": json.dumps(results)
            })
