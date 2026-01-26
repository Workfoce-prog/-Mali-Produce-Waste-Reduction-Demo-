import os
from flask import Flask, request, jsonify
import requests
from datetime import datetime

app = Flask(__name__)

APPS_SCRIPT_URL = os.getenv("APPS_SCRIPT_URL", "").strip()

def push(record):
    if not APPS_SCRIPT_URL:
        return False, "APPS_SCRIPT_URL not set"
    r = requests.post(APPS_SCRIPT_URL, json=record, timeout=15)
    if r.status_code == 200:
        return True, "ok"
    return False, f"{r.status_code}: {r.text[:200]}"

def normalize_payload(payload):
    # Try common fields from providers; user can extend this mapping.
    name = payload.get("name") or payload.get("FromName") or payload.get("senderName") or "unknown"
    phone = payload.get("phone") or payload.get("From") or payload.get("msisdn") or payload.get("sender") or ""
    body = payload.get("Body") or payload.get("text") or payload.get("message") or ""

    # Very simple parsing fallback: "TYPE=listing; CROP=Tomato; QTY=200; LOC=Bamako"
    crop = payload.get("crop") or ""
    qty = payload.get("quantity_kg") or ""
    loc = payload.get("location") or ""
    record_type = payload.get("record_type") or ""

    if body and (not crop or not qty or not loc or not record_type):
        parts = [p.strip() for p in body.split(";")]
        kv = {}
        for p in parts:
            if "=" in p:
                k,v = p.split("=",1)
                kv[k.strip().lower()] = v.strip()
        record_type = record_type or kv.get("type","")
        crop = crop or kv.get("crop","")
        qty = qty or kv.get("qty","")
        loc = loc or kv.get("loc","")

    return {
        "record_type": record_type,
        "name": name,
        "phone": phone,
        "crop": crop,
        "quantity_kg": qty,
        "location": loc,
        "date": datetime.utcnow().date().isoformat(),
        "notes": f"inbound webhook | raw={str(payload)[:500]}"
    }

@app.post("/sms")
def sms():
    payload = request.form.to_dict() if request.form else (request.json or {})
    rec = normalize_payload(payload)
    ok, msg = push(rec)
    return jsonify({"ok": ok, "message": msg, "record": rec})

@app.post("/whatsapp")
def whatsapp():
    payload = request.form.to_dict() if request.form else (request.json or {})
    rec = normalize_payload(payload)
    ok, msg = push(rec)
    return jsonify({"ok": ok, "message": msg, "record": rec})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
