import pathlib, time
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

DOCS_DIR = pathlib.Path(__file__).resolve().parents[1] / "docs"

class RAGKB:
    def __init__(self):
        self.docs = []
        self.ids = []
        for p in DOCS_DIR.glob("*.txt"):
            txt = p.read_text(encoding="utf-8")
            self.docs.append(txt)
            self.ids.append(p.name)
        self.vectorizer = TfidfVectorizer()
        self.X = self.vectorizer.fit_transform(self.docs)

    def query(self, q: str, k: int = 2):
        t0 = time.time()
        q_vec = self.vectorizer.transform([q])
        sims = cosine_similarity(q_vec, self.X).ravel()
        idxs = sims.argsort()[::-1][:k]
        results = []
        for i in idxs:
            results.append({"doc": self.ids[i], "text": self.docs[i], "score": float(sims[i])})
        latency = round((time.time()-t0)*1000,2)
        return results, latency

    def answer(self, q: str):
        results, latency = self.query(q)
        if results[0]["score"] < 0.1:
            return {"answer": "Sorry, I don't have knowledge on that.", "citations": [], "latency_ms": latency}
        answer = results[0]["text"]
        citations = [f"{r['doc']} (score {r['score']:.2f})" for r in results]
        return {"answer": answer, "citations": citations, "latency_ms": latency}
