from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health():
    r = client.get("/")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"

def test_generate_quote_math():
    payload = {
        "client": {"name": "Gulf Eng.", "contact": "omar@client.com", "lang": "en"},
        "currency": "SAR",
        "items": [
            {"sku": "ALR-SL-90W", "qty": 2, "unit_cost": 100, "margin_pct": 10},
            {"sku": "ALR-OBL-12V", "qty": 1, "unit_cost": 50, "margin_pct": 20}
        ],
        "delivery_terms": "DAP Dammam, 4 weeks",
        "notes": "Spec compliance required"
    }
    res = client.post("/quote", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert data["grand_total"] == 280.0
    assert data["line_totals"][0]["total"] == 220.0
    assert data["line_totals"][1]["total"] == 60.0
    assert "Hello Gulf Eng." in data["email_draft"]
