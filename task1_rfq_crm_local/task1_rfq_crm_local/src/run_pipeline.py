import pathlib, sys, traceback
from email import policy
from email.parser import BytesParser

from extract import extract_fields
from services import ensure_dirs, append_to_sheet, create_crm_opportunity, archive_attachments, write_auto_reply, alert, log_error

DATA = pathlib.Path(__file__).resolve().parents[1] / "data"
SAMPLES = DATA / "sample_emails"

def parse_eml(path: pathlib.Path):
    with path.open('rb') as f:
        msg = BytesParser(policy=policy.default).parse(f)
    subject = msg['subject'] or ''
    frm = msg['from'] or ''
    # Body: prefer plain, fallback to html stripped
    body = ""
    attachments = []
    if msg.is_multipart():
        for part in msg.walk():
            ctype = part.get_content_type()
            disp = part.get_content_disposition()
            if ctype == "text/plain" and disp != "attachment":
                body = part.get_content()
            elif disp == "attachment":
                # Save attachment to temp and return path
                fname = part.get_filename() or "attachment.bin"
                out = DATA / fname
                with out.open("wb") as fp:
                    fp.write(part.get_content())
                attachments.append(str(out))
    else:
        ctype = msg.get_content_type()
        if ctype == "text/plain":
            body = msg.get_content()
        else:
            body = msg.get_content()
    return frm, subject, body, attachments

def process_eml(path: pathlib.Path):
    try:
        frm, subject, body, attachments = parse_eml(path)
        fields = extract_fields(subject, body)
        append_to_sheet(fields)
        opp = create_crm_opportunity(fields)
        saved = archive_attachments(fields.get("rfq_id","TBD"), attachments)
        reply_path = write_auto_reply(fields.get("rfq_id","TBD"), frm, fields)
        alert(f"[RFQ] {fields.get('rfq_id','TBD')} from {frm} — {subject}")
        print(f"Processed: {path.name}\n  CRM: {opp['opportunity_name']}\n  Reply: {reply_path}\n  Saved: {len(saved)} attachment(s)")
    except Exception as e:
        log_error(f"{path.name}: {e}")
        traceback.print_exc()
        print(f"Error processing {path.name}: {e}", file=sys.stderr)

def main():
    ensure_dirs()
    files = sorted(SAMPLES.glob("*.eml"))
    if not files:
        print("No .eml files found in ./data/sample_emails")
        return
    for f in files:
        process_eml(f)

if __name__ == "__main__":
    main()
