from rag import RAGKB

def main():
    kb = RAGKB()
    print("RAG KB ready. Ask a question (type 'exit' to quit).")
    while True:
        q = input("Q: ").strip()
        if not q or q.lower() in {"exit","quit"}:
            break
        out = kb.answer(q)
        print("A:", out["answer"])
        print("Citations:", out["citations"])
        print("Latency (ms):", out["latency_ms"])

if __name__ == "__main__":
    main()
