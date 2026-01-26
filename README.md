# Mali Produce Waste Reduction – Full Demo App (V2)

This is a full demo app to reduce post-harvest produce waste in Mali, integrating:
1) Google Sheets live sync (Apps Script Web App)
2) SMS/WhatsApp intake (starter webhook service + instructions)
3) Multilingual UI (English / French / Bambara)
4) Roles (farmer / buyer / admin) with login
5) Cold-hub inventory dashboard
6) Impact metrics (waste reduction + value saved)
7) Payment hooks (CSA + storage payments placeholder)

## Run locally
```bash
pip install -r requirements.txt
streamlit run app.py
```

## Deploy (Streamlit Cloud)
- Push this repo to GitHub
- Deploy on Streamlit Cloud (main file: app.py)

## Google Sheets live sync (Option 1)
1. Create a Google Sheet and name a tab **records**
2. Go to Extensions → Apps Script and paste `apps_script/Code.gs`
3. Deploy → New deployment → Web App
   - Execute as: Me
   - Who has access: Anyone
4. Copy the Web App URL
5. In the Streamlit app, go to **Settings → Google Sync** and paste the URL

## SMS / WhatsApp intake (starter)
Streamlit apps can’t directly receive webhooks. Use the included lightweight webhook service:
- `integrations/webhook_service.py` (Flask)
It receives inbound SMS/WhatsApp payloads and writes them to the same Google Sheet via Apps Script.

Run:
```bash
pip install flask requests
python integrations/webhook_service.py
```

Then point your SMS provider webhook to:
- `POST /sms`
- `POST /whatsapp`

See `integrations/README_integrations.md`.

## Users (demo)
Default demo users are defined in `utils/auth_config.yaml`.
- admin / admin123
- farmer1 / farmer123
- buyer1 / buyer123

Change passwords before any real use.

## Data model
All records are written to:
- local CSV database: `data/app_db.csv`
- (optional) Google Sheet via Apps Script endpoint

---
**Note:** This is a demo accelerator. For production, use a real database, secure secrets, HTTPS webhooks, and proper IAM.
