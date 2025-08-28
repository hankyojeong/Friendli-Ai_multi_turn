# Friendli-Ai_multi_turn

## FastAPI Server

Run the HTTP server with:

```bash
uvicorn server:app --reload
```

The server exposes `POST /chat/{session_id}` for chatting with the LLM. Each
session maintains its own message history in memory.
