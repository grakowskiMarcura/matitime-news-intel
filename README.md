# Maritime News Intelligence App 🌊⚓

A **continuous LangChain-based platform** that collects maritime news and social posts, identifies industry leaders' voices, classifies content by sector, and ranks items by importance for a live feed or dashboard.

---

## 📑 Table of Contents

- [What it does](#what-it-does)
- [Features](#features)
- [Project structure](#project-structure)
- [Tech stack](#tech-stack)
- [Quick start](#quick-start)
- [Environment variables](#environment-variables)
- [API examples](#api-examples)
- [Demo pipeline](#demo-pipeline)
- [Ranking example](#ranking-example)
- [Testing](#testing)
- [Roadmap](#roadmap)
- [Contributing & License](#contributing--license)

---

## 🚀 What it does

Continuously:

1. Scrapes/collects posts from social platforms and industry sites.
2. Cleans and deduplicates content.
3. Uses LangChain + LLMs to detect **voice type** (industry leader, journalist, public), tag **sector**, and optionally sentiment.
4. Generates embeddings for semantic search and ranks messages by importance (authority, engagement, recency, relevance).
5. Stores results in Postgres (Supabase) with `pgvector` and serves them via a FastAPI backend consumed by a React dashboard.

---

## ✨ Features

- Continuous ingestion (scheduled via Prefect or Celery).
- Multi-source connectors (X/Twitter, LinkedIn, RSS feeds, industry websites).
- Voice detection: Industry leader / Journalist / Public.
- Sector tagging: Tankers, Dry Bulk, Containers, LNG, Regulation, Geopolitics, Green shipping, etc.
- Importance scoring (authority + engagement + recency + relevance).
- Semantic search (vector DB / pgvector).
- FastAPI endpoints for feed, search, and summaries.
- Optional alerting & trend detection.

---

## 📂 Project structure

```text
maritime-news-intel/
├── backend/                # FastAPI + LangChain pipeline
│   ├── app/
│   │   ├── main.py
│   │   ├── api/
│   │   │   ├── routes_feed.py
│   │   │   ├── routes_search.py
│   │   │   └── routes_summary.py
│   │   ├── core/
│   │   │   ├── config.py
│   │   │   ├── db.py
│   │   │   └── logger.py
│   │   ├── pipeline/
│   │   │   ├── ingest.py
│   │   │   ├── preprocess.py
│   │   │   ├── classify.py
│   │   │   ├── rank.py
│   │   │   └── store.py
│   │   └── models/
│   │       └── document.py
│   └── requirements.txt
│
├── orchestrator/           # Prefect flows / scheduling
│   └── flows/news_pipeline.py
│
├── frontend/               # React + Vite + Tailwind + ShadCN
│   ├── src/
│   └── package.json
│
├── docker-compose.yml
├── .env.example
└── README.md
```

---

## 🛠 Tech stack

- **Python 3.10+**
- **LangChain** for LLM orchestration
- **FastAPI** backend
- **Supabase / Postgres** with `pgvector`
- **Prefect** (or Celery) for scheduled pipelines
- **React + Vite + Tailwind + ShadCN UI** frontend
- **Docker / docker-compose** for local development

---

## ⚡ Quick start

### 1. Clone the repo

```bash
git clone https://github.com/your-org/maritime-news-intel.git
cd maritime-news-intel
```

### 2. Setup environment

Copy `.env.example` → `.env` and fill in keys.

### 3. Run with Docker

```bash
docker-compose up --build
```

- Backend: `http://localhost:8000`
- Frontend: `http://localhost:3000`
- Prefect UI (if enabled): `http://localhost:4200`

### 4. Local dev (without Docker)

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r backend/requirements.txt
uvicorn backend.app.main:app --reload --port 8000
```

---

## 🔑 Environment variables

`.env.example`:

```ini
# Database
DATABASE_URL=postgresql+psycopg2://postgres:password@db:5432/maritime

# OpenAI / LLM
OPENAI_API_KEY=sk-...

# Vector DB (optional external service)
PINECONE_API_KEY=...
PINECONE_ENVIRONMENT=...

# Prefect
PREFECT_API_URL=http://localhost:4200

# Social media connectors
TWITTER_BEARER_TOKEN=...
LINKEDIN_COOKIES=...
SUPABASE_URL=https://xyz.supabase.co
SUPABASE_KEY=service_role_key
```

---

## 📡 API examples

**GET** `/feed?sector=tanker&limit=20`  - Returns the latest ranked posts for the tanker sector.\
**GET** `/search?q=sanctions&limit=10`  - Semantic + keyword search.\
**GET** `/summary?sector=bulk&period=24h`  - Digest summary for bulk sector in the last 24 hours.

```bash
curl "http://localhost:8000/feed?sector=tanker&limit=5"
```

---

## 🧪 Demo pipeline

Minimal fake ingest for testing:

```python
# backend/app/pipeline/fake_ingest.py
from datetime import datetime
from backend.app.models.document import Document

def generate_fake_docs():
    return [
        Document(
            id="fake-1",
            text="CEO of BigShipCo: new sanctions will disrupt crude tanker routes.",
            author="Jane Captain",
            platform="X",
            timestamp=datetime.utcnow().isoformat(),
            engagement={"likes": 124, "retweets": 30}
        )
    ]
```

Run:

```bash
python backend/app/pipeline/fake_ingest.py
```

---

## 📊 Ranking example

```python
def score_document(doc, authority_map):
    source_score = authority_map.get(doc.source, 0.3)
    engagement = doc.metadata.get("engagement", {})
    engagement_score = (engagement.get("likes",0) + engagement.get("retweets",0)*2)/100.0
    recency_score = 1.0  # replace with time decay logic
    relevance_score = 0.8  # from cosine similarity

    return (
        0.4 * source_score +
        0.25 * min(1, engagement_score) +
        0.2 * recency_score +
        0.15 * relevance_score
    )
```

---

## 🧪 Testing

```bash
pytest backend/tests/
```

---

## 📈 Roadmap

-

---

## 🤝 Contributing & License

Contributions welcome — open an issue or PR.\
Licensed under **MIT**.

