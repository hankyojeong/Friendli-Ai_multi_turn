import os
from typing import Dict, List

from fastapi import FastAPI
from pydantic import BaseModel

from utils import make_client, call_llm

app = FastAPI()

# In-memory storage of conversation per session
_sessions: Dict[str, List[Dict[str, str]]] = {}

MODEL = os.getenv("FRIENDLI_MODEL", "gpt-4o-mini")
DEFAULT_SYSTEM = os.getenv("SYSTEM_PROMPT", "You are a helpful assistant.")


class ChatRequest(BaseModel):
    message: str
    system_prompt: str | None = None


@app.post("/chat/{session_id}")
async def chat(session_id: str, req: ChatRequest):
    """Handle a chat message for the given session."""
    messages = _sessions.setdefault(session_id, [])

    # Initialize session with system prompt when first message arrives
    if not messages:
        system = req.system_prompt or DEFAULT_SYSTEM
        messages.append({"role": "system", "content": system})

    # Append user message
    messages.append({"role": "user", "content": req.message})

    client = make_client()
    answer = call_llm(client, MODEL, messages=messages)
    messages.append({"role": "assistant", "content": answer})

    return {"question": req.message, "answer": answer}
