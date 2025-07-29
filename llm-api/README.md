# LLM API

A minimal REST API for prompt-based text generation using FastAPI. Works fully offline with stubbed or local LLM responses.

## Features
- POST `/generate` endpoint: accepts `{ "prompt": "..." }`, returns `{ "response": "..." }`
- Logs every request/response to `logs/log.jsonl` (one JSON object per line)
- No cloud APIs. Works offline.
- Modular, clean codebase with backend abstraction
- **Multi-backend LLM support:** Ollama, HuggingFace, OpenAI, Claude, or stub
- **Configurable backend selection** via environment variables
- **Health check and configuration endpoints**
- **Proper error handling and logging**

## Setup

1. **Clone the repo**

2. **Install dependencies**

```bash
cd llm-api
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3. **Configure the API**

Copy the example environment file and customize it:

```bash
cp env.example .env
# Edit .env with your preferred settings
```

**Key configuration options:**
- `LLM_BACKEND`: Choose backend (`ollama`, `huggingface`, `openai`, `claude`, `stub`)
- `OLLAMA_MODEL`: Model name for Ollama (default: `llama2`)
- `OLLAMA_URL`: Ollama server URL (default: `http://localhost:11434`)

4. **Backend-Specific Setup**

### Ollama (Recommended for local use)
- Download and install Ollama: https://ollama.com/download
- Start Ollama (it runs as a background service)
- Pull a model:

```bash
ollama pull llama2
```

### Other Backends
- **HuggingFace**: Set `HF_MODE`, `HF_MODEL`, and optionally `HF_API_KEY`
- **OpenAI**: Set `OPENAI_API_KEY` and optionally `OPENAI_MODEL`
- **Claude**: Set `CLAUDE_API_KEY` and optionally `CLAUDE_MODEL`

5. **Run the API**

```bash
uvicorn app.main:app --reload
```

6. **Test the endpoints**

**Generate a response:**
```bash
curl -X POST http://localhost:8000/generate \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Hello, world!"}'
```

**Health check:**
```bash
curl http://localhost:8000/health
```

**View configuration:**
```bash
curl http://localhost:8000/config
```

## API Endpoints

### POST `/generate`
Generate a response for a given prompt.

**Request:**
```json
{
  "prompt": "Your prompt here"
}
```

**Response:**
```json
{
  "response": "Generated response text"
}
```

### GET `/health`
Health check endpoint.

**Response:**
```json
{
  "status": "healthy",
  "backend": "ollama",
  "timestamp": 1234567890.123
}
```

### GET `/config`
Get current configuration (without sensitive data).

**Response:**
```json
{
  "backend": "ollama",
  "ollama_model": "llama2",
  "ollama_url": "http://localhost:11434",
  "log_file": "logs/log.jsonl"
}
```

## Project Structure

```
llm-api/
├── app/
│   ├── main.py                    # FastAPI app entry
│   ├── generator.py               # Main generation logic
│   ├── config.py                  # Configuration management
│   ├── logger.py                  # JSONL logging utility
│   └── backends/                  # Backend implementations
│       ├── __init__.py
│       ├── base.py                # Abstract base class
│       ├── factory.py             # Backend factory
│       ├── ollama.py              # Ollama backend
│       └── stub.py                # Stub backend
├── logs/
│   └── log.jsonl                  # Append-only log
├── requirements.txt               # Dependencies
├── env.example                    # Example environment file
├── LLM-API.postman_collection.json # Postman collection
└── README.md                      # This file
```

## Configuration

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `LLM_BACKEND` | Which LLM backend to use | `ollama` | No |
| `OLLAMA_MODEL` | Ollama model name | `llama2` | No |
| `OLLAMA_URL` | Ollama server URL | `http://localhost:11434` | No |
| `HF_MODE` | HuggingFace mode (`local`/`cloud`) | - | No |
| `HF_MODEL` | HuggingFace model name/path | - | No |
| `HF_API_KEY` | HuggingFace API key | - | No |
| `OPENAI_API_KEY` | OpenAI API key | - | No |
| `OPENAI_MODEL` | OpenAI model name | `gpt-3.5-turbo` | No |
| `CLAUDE_API_KEY` | Anthropic API key | - | No |
| `CLAUDE_MODEL` | Claude model name | `claude-3-sonnet-20240229` | No |
| `LOG_FILE` | Log file path | `logs/log.jsonl` | No |

## Architecture

The API uses a clean, extensible architecture:

- **Configuration Management**: Uses `pydantic-settings` for type-safe configuration
- **Backend Abstraction**: Abstract base class for all LLM backends
- **Factory Pattern**: Backend factory for creating and caching backend instances
- **Error Handling**: Proper exception hierarchy and graceful fallbacks
- **Logging**: Structured logging with performance metrics

## Notes
- All logs are stored in `logs/log.jsonl` (one JSON object per line)
- If a backend is not available or fails, the API will automatically fallback to the stub backend
- Backend selection is global (all requests use the same backend)
- HuggingFace, OpenAI, and Claude backends are stubbed for now (TODO: implement)
- The API includes performance metrics (duration) in logs 