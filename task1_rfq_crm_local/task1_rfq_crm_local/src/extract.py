\
import re
from typing import Dict, List, Tuple

SKU_QTY_RE = re.compile(r"(?P<sku>[A-Z0-9\-]{3,})\s*[xX]\s*(?P<qty>\d+)", re.MULTILINE)
INCOTERMS_RE = re.compile(r"\b(FOB|CIF|CFR|DAP|DDP|EXW)\b", re.IGNORECASE)
CITY_RE = re.compile(r"\b(Dammam|Riyadh|Jeddah|Dubai|Doha|Manama|Kuwait City)\b", re.IGNORECASE)
RFQ_ID_RE = re.compile(r"\bRFQ[-\s:]*(\d{3,})\b", re.IGNORECASE)
COMPANY_RE = re.compile(r"Company[:\-\s]*([A-Za-z0-9 &.,]+)")
CLIENT_RE = re.compile(r"(?:Regards|Best|Sincerely|Thanks)[,\n ]+([A-Za-z .'-]{3,})", re.IGNORECASE)

def parse_items(text: str) -> List[Tuple[str, int]]:
    items = []
    for m in SKU_QTY_RE.finditer(text):
        sku = m.group("sku")
        qty = int(m.group("qty"))
        items.append((sku, qty))
    return items

def extract_fields(subject: str, body: str) -> Dict:
    items = parse_items(body)
    incoterms = (INCOTERMS_RE.search(body) or INCOTERMS_RE.search(subject))
    incoterms = incoterms.group(0).upper() if incoterms else ""
    city = (CITY_RE.search(body) or CITY_RE.search(subject))
    city = city.group(0).title() if city else ""
    rfq_id = (RFQ_ID_RE.search(subject) or RFQ_ID_RE.search(body))
    rfq_id = rfq_id.group(1) if rfq_id else ""
    company = (COMPANY_RE.search(body) or COMPANY_RE.search(subject))
    company = company.group(1).strip() if company else ""
    client = (CLIENT_RE.search(body) or CLIENT_RE.search(subject))
    client = client.group(1).strip() if client else ""

    return {
        "rfq_id": rfq_id or "TBD",
        "incoterms": incoterms,
        "delivery_city": city,
        "company": company or "Unknown Co.",
        "client_name": client or "Procurement",
        "items": [{"sku": s, "qty": q} for s, q in items] or [],
    }
