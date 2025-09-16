from fastapi import FastAPI, Query
from app.rag import RAGKB

app = FastAPI(title="RAG KB",
              description="Simple local RAG Q&A with citations")

kb = RAGKB()


@app.get("/query")
def query(q: str = Query(..., description="Question in English")):
    return kb.answer(q)
