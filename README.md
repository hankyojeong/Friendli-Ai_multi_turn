# Friendli-Ai_multi_turn

Simple FastAPI application demonstrating multi-turn conversations with a
Friendli-powered language model.

## Credentials

This repository is configured to work without environment variables.  Update the
placeholders in `utils/llm_client.py` with your own `DEFAULT_API_KEY` and
`DEFAULT_TEAM_ID` values before running the server.

## Running

1. Install dependencies:

   ```bash
   pip install fastapi uvicorn openai
   ```

2. Start the web server:

   ```bash
   uvicorn server:app --reload
   ```

3. Open [http://localhost:8000/](http://localhost:8000/) in your browser and
   chat with the model.

