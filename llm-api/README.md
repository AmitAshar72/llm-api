# LLM API

A minimal REST API for prompt-based text generation using FastAPI. Works fully offline with stubbed or local LLM responses.

## Features
- POST `/generate` endpoint: accepts `{ "prompt": "..." }`, returns `{ "response": "..." }`
- Logs every request/response to `logs/log.jsonl` (one JSON object per line)
- No cloud APIs. Works offline.
- Modular, clean codebase

## Setup

1. **Clone the repo**

2. **Install dependencies**

```bash
cd llm-api
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3. **Run the API**

```bash
uvicorn app.main:app --reload
```

4. **Test the endpoint**

```bash
curl -X POST http://localhost:8000/generate \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Hello, world!"}'
```

Response:
```json
{"response": "This is a dummy response to: Hello, world!"}
```

## Project Structure

```
llm-api/
├── app/
│   ├── main.py            # FastAPI app entry
│   ├── generator.py       # Handles response generation (stubbed or optional LLM)
│   └── logger.py          # JSONL logging utility
├── logs/
│   └── log.jsonl          # Append-only log
├── requirements.txt       # Minimal dependencies
└── README.md              # Setup + notes
```

## Notes
- To use a real local LLM (e.g., Ollama, HuggingFace), extend `app/generator.py`.
- All logs are stored in `logs/log.jsonl` (one JSON object per line).
- No cloud API keys required. 