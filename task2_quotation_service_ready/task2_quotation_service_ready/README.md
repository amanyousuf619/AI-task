# Task 2 — Quotation Microservice (FastAPI)

Fully runnable, no secrets. Exposes `/quote` which returns line totals, a grand total,
and a short email draft. Includes tests and Dockerfile.

## Quickstart (local)
```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Open API docs:
- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc:      http://127.0.0.1:8000/redoc

### Example
```bash
curl -X POST http://127.0.0.1:8000/quote   -H "Content-Type: application/json"   -d '{
    "client": {"name": "Gulf Eng.", "contact": "omar@client.com", "lang": "en"},
    "currency": "SAR",
    "items": [
      {"sku": "ALR-SL-90W", "qty": 2, "unit_cost": 100, "margin_pct": 10},
      {"sku": "ALR-OBL-12V", "qty": 1, "unit_cost": 50, "margin_pct": 20}
    ],
    "delivery_terms": "DAP Dammam, 4 weeks",
    "notes": "Spec compliance required"
  }'
```

## Run tests
```bash
pip install -r requirements.txt
pytest -q
```

## Docker
```bash
docker build -t quotation_service .
docker run -p 8000:8000 quotation_service
```
