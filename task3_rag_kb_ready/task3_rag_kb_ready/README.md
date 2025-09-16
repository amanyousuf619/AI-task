# Task 3 — RAG Knowledge Base (Local, No Secrets)

A simple retrieval‑augmented Q&A system in English.  
Uses **TF‑IDF embeddings** and **cosine similarity** (no API keys, no cloud).

## Features
- Ingest 3–5 sample docs from `./docs`
- Chunk, embed, index with scikit‑learn TF‑IDF
- Query with cosine similarity
- Return **answer with citations**
- CLI interface (`python app/rag_cli.py`)
- Minimal web interface (`uvicorn app.web:app --reload`)
- Graceful refusal if question is out‑of‑scope
- Latency printed per query

## Quickstart (CLI)
```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python app/rag_cli.py
```

## Web UI
```bash
uvicorn app.web:app --reload
# then open http://127.0.0.1:8000/query?q=delivery+timeline
```

## Files
- `docs/` sample documents
- `app/rag.py` core pipeline
- `app/rag_cli.py` command‑line interface
- `app/web.py` FastAPI endpoint
