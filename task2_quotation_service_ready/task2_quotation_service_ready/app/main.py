from fastapi import FastAPI, Body
from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional

app = FastAPI(
    title="Quotation Microservice",
    version="1.0.0",
    description="""
Compute line totals and a grand total for a set of items.
Also returns a simple email draft summarizing the quote.

**Formula:** `unit_cost × (1 + margin_pct/100) × qty`
"""
)

class Item(BaseModel):
    sku: str = Field(..., description="Stock keeping unit / part number")
    qty: int = Field(ge=1, description="Quantity")
    unit_cost: float = Field(ge=0, description="Unit cost (pre-margin)")
    margin_pct: float = Field(ge=0, description="Margin percentage to apply")

class Client(BaseModel):
    name: str
    contact: str
    lang: str = Field(default="en", description="Language code (unused in this minimal service)")

class QuoteRequest(BaseModel):
    client: Client
    currency: str = Field(default="USD", description="ISO currency code (not validated here)")
    items: List[Item]
    delivery_terms: str = ""
    notes: str = ""

class LineTotal(BaseModel):
    sku: str
    qty: int
    total: float

class QuoteResponse(BaseModel):
    model_config = ConfigDict(json_schema_extra={
        "example": {
            "line_totals": [
                {"sku": "ALR-SL-90W", "qty": 2, "total": 220.0},
                {"sku": "ALR-OBL-12V", "qty": 1, "total": 60.0}
            ],
            "grand_total": 280.0,
            "email_draft": "Hello Gulf Eng.,\nTotal Quote: 280.0 SAR\nDelivery: DAP Dammam, 4 weeks\nNotes: Spec compliance required"
        }
    })
    line_totals: List[LineTotal]
    grand_total: float
    email_draft: str

@app.get("/", tags=["health"])
def health():
    return {"status": "ok"}

@app.post("/quote", response_model=QuoteResponse, tags=["quote"])
def generate_quote(req: QuoteRequest = Body(..., examples={
    "example1": {
        "summary": "Streetlights with margin",
        "description": "Two line items with margins and DAP terms",
        "value": {
            "client": {"name": "Gulf Eng.", "contact": "omar@client.com", "lang": "en"},
            "currency": "SAR",
            "items": [
                {"sku": "ALR-SL-90W", "qty": 2, "unit_cost": 100, "margin_pct": 10},
                {"sku": "ALR-OBL-12V", "qty": 1, "unit_cost": 50, "margin_pct": 20}
            ],
            "delivery_terms": "DAP Dammam, 4 weeks",
            "notes": "Spec compliance required"
        }
    }
})):
    line_totals = []
    grand_total = 0.0
    for it in req.items:
        total = it.unit_cost * (1 + it.margin_pct / 100.0) * it.qty
        total = round(total, 2)
        line_totals.append(LineTotal(sku=it.sku, qty=it.qty, total=total))
        grand_total += total
    grand_total = round(grand_total, 2)

    email_draft = (
        f"Hello {req.client.name},\n"
        f"Total Quote: {grand_total} {req.currency}\n"
        f"Delivery: {req.delivery_terms}\n"
        f"Notes: {req.notes}"
    )
    return QuoteResponse(line_totals=line_totals, grand_total=grand_total, email_draft=email_draft)
