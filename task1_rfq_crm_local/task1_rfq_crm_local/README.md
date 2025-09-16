# Task 1 — RFQ → CRM (Local, No Secrets, Fully Runnable)

This package simulates the full RFQ pipeline **locally** using sample `.eml` files.
It requires **no API keys**, **no Gmail/Slack/Google**. Everything is written to `./data`.

**Pipeline steps for each RFQ email (.eml):**
1) Parse the email and **extract fields** (client, company, RFQ id, items, incoterms, delivery city)
2) **Append a row** to `./data/rfq_log.csv` (acts like Google Sheet)
3) **Create an Opportunity** in a mock CRM: append JSON line to `./data/crm_opportunities.jsonl`
4) **Archive attachments** to `./data/drive/<RFQ_ID>/`
5) **Generate an Auto‑Reply** (EN) into `./data/outbox/reply_<RFQ_ID>.txt`
6) **Write an internal alert** to `./data/alerts.log`
7) **Log errors** to `./data/error.log`

## Quickstart
```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python src/run_pipeline.py
```

### Where to put inputs
- Drop `.eml` files into `./data/sample_emails/`. Two examples are already included.

### Outputs
- Sheet (CSV): `./data/rfq_log.csv`
- CRM log (JSONL): `./data/crm_opportunities.jsonl`
- Archived attachments: `./data/drive/<RFQ_ID>/...`
- Auto‑reply drafts: `./data/outbox/reply_<RFQ_ID>.txt`
- Alerts: `./data/alerts.log`
- Errors: `./data/error.log`

## Extending to real services
- Replace writers in `services.py` with Google Sheets API, Drive API, Slack SDK, and SMTP or Gmail API calls.
- The injection points are already isolated.

## Testing notes
- The parser uses light regex for SKUs and quantities (e.g., `ALR-SL-90W x 2`). Adjust `extract.py` to your real RFQ formats.
