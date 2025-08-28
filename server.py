from fastapi import FastAPI
from pydantic import BaseModel
from typing import Dict, List

from utils import make_client, call_llm

app = FastAPI()
client = make_client()

# Load default system prompt used by existing scripts
with open("system_prompt/Prompt3.txt", encoding="utf-8") as f:
    SYSTEM_PROMPT = f.read()

# In-memory storage of conversation histories
sessions: Dict[str, List[Dict[str, str]]] = {}

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    content: str
    needs_reply: bool

@app.post("/chat/{session_id}", response_model=ChatResponse)
async def chat(session_id: str, req: ChatRequest) -> ChatResponse:
    """Chat endpoint that maintains session-specific conversation."""
    history = sessions.setdefault(session_id, [])

    result = call_llm(
        client,
        model="gpt-3.5-turbo",
        system_prompt=SYSTEM_PROMPT,
        user_question=req.message,
        history=history,
        user_reply=req.message if history else None,
        multi_turn=True,
    )

    # Record dialogue
    history.append({"role": "user", "content": req.message})
    history.append({"role": "assistant", "content": result["content"]})

    if not result["needs_reply"]:
        # Conversation finished; clean up session
        sessions.pop(session_id, None)

    return ChatResponse(**result)
