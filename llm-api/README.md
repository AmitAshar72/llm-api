# LLM API

A minimal REST API for prompt-based text generation using FastAPI. Works fully offline with stubbed or local LLM responses.

## Features
- POST `/generate` endpoint: accepts `{ "prompt": "..." }`, returns `{ "response": "..." }`
- Logs every request/response to `logs/log.jsonl` (one JSON object per line)
- No cloud APIs. Works offline.
- Modular, clean codebase
- **Optional:** Integrates with [Ollama](https://ollama.com/) for local LLMs (default: `llama2`)

## Setup

1. **Clone the repo**

2. **Install dependencies**

```bash
cd llm-api
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3. **(Optional) Install Ollama for local LLMs**

- Download and install Ollama: https://ollama.com/download
- Start Ollama (it runs as a background service)
- Pull a model (default is `llama2`):

```bash
ollama pull llama2
```

- To use a different model, pull it (e.g., `ollama pull phi`) and set the environment variable:

```bash
# On Linux/macOS
export OLLAMA_MODEL=phi
# On Windows (cmd)
set OLLAMA_MODEL=phi
# On Windows (PowerShell)
$env:OLLAMA_MODEL="phi"
```

4. **Run the API**

```bash
uvicorn app.main:app --reload
```

5. **Test the endpoint**

```bash
curl -X POST http://localhost:8000/generate \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Hello, world!"}'
```

Response (if Ollama is running):
```json
{"response": "...LLM output..."}
```

Response (if Ollama is not running):
```json
{"response": "This is a dummy response to: Hello, world!"}
```

## Project Structure

```
llm-api/
├── app/
│   ├── main.py            # FastAPI app entry
│   ├── generator.py       # Handles response generation (Ollama or stub)
│   └── logger.py          # JSONL logging utility
├── logs/
│   └── log.jsonl          # Append-only log
├── requirements.txt       # Minimal dependencies
├── LLM-API.postman_collection.json # Postman collection
└── README.md              # Setup + notes
```

## Notes
- To use a real local LLM (e.g., Ollama, HuggingFace), extend `app/generator.py`.
- All logs are stored in `logs/log.jsonl` (one JSON object per line).
- No cloud API keys required.
- If Ollama is not running or fails, the API will return a stubbed response.
- The Ollama model can be changed by setting the `OLLAMA_MODEL` environment variable (default: `llama2`). 