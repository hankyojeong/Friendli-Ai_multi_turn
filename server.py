from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import Dict, List

from utils import make_client, call_llm

app = FastAPI()

# CORS (allow all for simple browser testing)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve static files (index.html, etc.)
app.mount("/static", StaticFiles(directory="static"), name="static")

client = make_client()

# Load default system prompt used by existing scripts
try:
    with open("system_prompt/Prompt3.txt", encoding="utf-8") as f:
        SYSTEM_PROMPT = f.read()
except FileNotFoundError:
    SYSTEM_PROMPT = "You are a helpful assistant."

# In-memory storage of conversation histories
sessions: Dict[str, List[Dict[str, str]]] = {}


class ChatRequest(BaseModel):
    message: str


class ChatResponse(BaseModel):
    content: str
    needs_reply: bool


@app.get("/", response_class=HTMLResponse)
async def index() -> HTMLResponse:
    """Serve a simple web UI for chatting."""
    with open("static/index.html", encoding="utf-8") as f:
        return HTMLResponse(f.read())


@app.post("/chat/{session_id}", response_model=ChatResponse)
async def chat(session_id: str, req: ChatRequest) -> ChatResponse:
    """Chat endpoint that maintains session-specific conversation."""
    history = sessions.setdefault(session_id, [])

    result = call_llm(
        client=client,
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
