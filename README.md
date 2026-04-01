# support-bot-api

![Python](https://img.shields.io/badge/python-3.11+-blue)
![FastAPI](https://img.shields.io/badge/API-FastAPI-009688)
![Groq](https://img.shields.io/badge/AI-Groq%20%2F%20switchable-orange)
![License](https://img.shields.io/badge/license-MIT-lightgrey)

> A customer support chatbot with FAQ matching and AI fallback. Built with FastAPI, a clean HTML chat UI, and switchable AI providers. Answers from your FAQ first — falls back to AI only when needed.

## Architecture

```
User message → FAQ fuzzy matcher → match found → FAQ answer
                      ↓
               no match found
                      ↓
           Switchable AI provider → AI answer
     (Groq · OpenAI · Anthropic · Ollama)
```

## Features

- FAQ-first responses — fast, consistent, free
- AI fallback for questions not in FAQ
- Fuzzy matching with configurable threshold
- Clean HTML chat UI — no framework needed
- FastAPI REST API with `/chat` and `/health` endpoints
- Fully local mode via Ollama (no API key needed)

## Quick start

### 1. Clone and set up environment

```bash
git clone https://github.com/wahhabriaz/support-bot-api
cd support-bot-api
python -m venv .venv

# Windows
.venv\Scripts\activate

# Mac/Linux
source .venv/bin/activate

pip install -e .
```

### 2. Set up `.env`

```bash
cp .env.example .env
```

### 3. Run locally free with Ollama

Install Ollama from https://ollama.com/download then:

```bash
ollama pull llama3.2
```

Set your `.env`:

```env
SB_PROVIDER=ollama
SB_MODEL=llama3.2
SB_FAQ_PATH=./data/faq.json
SB_SIMILARITY_THRESHOLD=0.75
```

### 4. Run the server

```bash
uvicorn support_bot.api:app --reload --host 0.0.0.0 --port 8000
```

Open http://localhost:8000 in your browser.

## API endpoints

| Method | Endpoint  | Description                 |
| ------ | --------- | --------------------------- |
| `GET`  | `/`       | Chat UI                     |
| `POST` | `/chat`   | Send a message, get a reply |
| `GET`  | `/health` | Health check                |

### Chat request example

```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "What is your refund policy?", "history": []}'
```

### Response

```json
{
  "answer": "We offer a 30-day full refund on all orders.",
  "source": "faq"
}
```

`source` is either `faq` or `ai` so you always know where the answer came from.

## Customizing the FAQ

Edit `data/faq.json` — add as many question/answer pairs as you need:

```json
[
  {
    "id": 1,
    "question": "What is your refund policy?",
    "answer": "We offer a 30-day full refund on all orders."
  }
]
```

## Switching AI providers

Change `SB_PROVIDER` in `.env`:

| Provider       | Value       | Model example             | API key needed  |
| -------------- | ----------- | ------------------------- | --------------- |
| Ollama (local) | `ollama`    | `llama3.2`                | No              |
| Groq (free)    | `groq`      | `llama3-8b-8192`          | Yes (free tier) |
| OpenAI         | `openai`    | `gpt-4o-mini`             | Yes             |
| Anthropic      | `anthropic` | `claude-3-haiku-20240307` | Yes             |

## Environment variables

| Variable                  | Default           | Description                 |
| ------------------------- | ----------------- | --------------------------- |
| `SB_PROVIDER`             | `groq`            | AI provider                 |
| `SB_MODEL`                | `llama3-8b-8192`  | Model name                  |
| `SB_FAQ_PATH`             | `./data/faq.json` | Path to FAQ file            |
| `SB_SIMILARITY_THRESHOLD` | `0.75`            | Minimum score for FAQ match |
| `SB_HOST`                 | `0.0.0.0`         | Server host                 |
| `SB_PORT`                 | `8000`            | Server port                 |
| `SB_GROQ_API_KEY`         | —                 | Groq API key                |
| `SB_OPENAI_API_KEY`       | —                 | OpenAI API key              |
| `SB_ANTHROPIC_API_KEY`    | —                 | Anthropic API key           |

## Project structure

```
support-bot-api/
├── src/support_bot/
│   ├── __init__.py       # Settings
│   ├── providers.py      # Switchable AI providers
│   ├── faq.py            # FAQ loader and fuzzy matcher
│   ├── bot.py            # Bot logic with fallback
│   ├── api.py            # FastAPI routes
│   └── logger.py
├── static/index.html     # Chat UI
├── data/faq.json         # FAQ knowledge base
└── .env.example
```

## Tech stack

Python 3.11 · FastAPI · Uvicorn · LangChain · Groq · OpenAI · Anthropic · Ollama
