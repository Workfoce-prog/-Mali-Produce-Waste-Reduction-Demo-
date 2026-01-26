# Integrations (SMS / WhatsApp) – Starter

Streamlit does not accept inbound webhooks reliably, so use a small webhook service.

## 1) Run the webhook service
```bash
pip install flask requests
python webhook_service.py
```

## 2) Configure environment
Set:
- APPS_SCRIPT_URL = your deployed Apps Script Web App URL

Example (Linux/macOS):
```bash
export APPS_SCRIPT_URL="https://script.google.com/macros/s/XXXX/exec"
```

Windows PowerShell:
```powershell
setx APPS_SCRIPT_URL "https://script.google.com/macros/s/XXXX/exec"
```

## 3) Point provider webhooks
- SMS: POST http://YOUR_SERVER:5000/sms
- WhatsApp: POST http://YOUR_SERVER:5000/whatsapp

## Payload format
This service accepts many formats. Minimum fields:
- name
- phone
- crop
- quantity_kg
- location
- record_type: listing or demand

You can map Twilio or Africa's Talking payloads in the file.
