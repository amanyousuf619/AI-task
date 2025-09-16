import csv, json, os, pathlib, datetime, shutil

DATA = pathlib.Path(__file__).resolve().parents[1] / "data"
SHEET_CSV = DATA / "rfq_log.csv"
CRM_JSONL = DATA / "crm_opportunities.jsonl"
DRIVE_DIR = DATA / "drive"
OUTBOX_DIR = DATA / "outbox"
ALERTS_LOG = DATA / "alerts.log"
ERROR_LOG = DATA / "error.log"

def ensure_dirs():
    for p in [DATA, DRIVE_DIR, OUTBOX_DIR]:
        p.mkdir(parents=True, exist_ok=True)

def append_to_sheet(row: dict):
    header = ["timestamp","rfq_id","company","client_name","incoterms","delivery_city","items"]
    write_header = not SHEET_CSV.exists()
    with SHEET_CSV.open("a", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=header)
        if write_header:
            w.writeheader()
        w.writerow({
            "timestamp": datetime.datetime.utcnow().isoformat(),
            "rfq_id": row.get("rfq_id",""),
            "company": row.get("company",""),
            "client_name": row.get("client_name",""),
            "incoterms": row.get("incoterms",""),
            "delivery_city": row.get("delivery_city",""),
            "items": json.dumps(row.get("items",[]), ensure_ascii=False)
        })

def create_crm_opportunity(row: dict):
    payload = {
        "created_at": datetime.datetime.utcnow().isoformat(),
        "opportunity_name": f"RFQ {row.get('rfq_id','TBD')} - {row.get('company','')}",
        "stage": "New",
        "amount_estimate": 0,
        "meta": row,
    }
    with CRM_JSONL.open("a", encoding="utf-8") as f:
        f.write(json.dumps(payload, ensure_ascii=False) + "\n")
    return payload

def archive_attachments(rfq_id: str, attachments: list):
    target = DRIVE_DIR / (rfq_id or "TBD")
    target.mkdir(parents=True, exist_ok=True)
    saved = []
    for src in attachments:
        dst = target / os.path.basename(src)
        shutil.copyfile(src, dst)
        saved.append(str(dst))
    return saved

def write_auto_reply(rfq_id: str, to_addr: str, row: dict):
    OUTBOX_DIR.mkdir(parents=True, exist_ok=True)
    path = OUTBOX_DIR / f"reply_{rfq_id or 'TBD'}.txt"
    items_str = ', '.join([f"{i['sku']} x {i['qty']}" for i in row.get('items',[])])
    body = (
        f"Subject: Re: RFQ {rfq_id or 'TBD'} — Received\n"
        f"To: {to_addr}\n\n"
        "Hello,\n\n"
        "Thank you for your RFQ. Our team has logged your request and will respond with a quotation shortly.\n\n"
        f"Company: {row.get('company')}\n"
        f"Incoterms: {row.get('incoterms','')}\n"
        f"Delivery City: {row.get('delivery_city','')}\n"
        f"Items: {items_str}\n\n"
        "Best regards,\nSales"
    )
    path.write_text(body, encoding="utf-8")
    return str(path)

def alert(message: str):
    with ALERTS_LOG.open("a", encoding="utf-8") as f:
        f.write(message + "\n")

def log_error(error: str):
    with ERROR_LOG.open("a", encoding="utf-8") as f:
        f.write(error + "\n")
