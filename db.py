import os
import pandas as pd
from datetime import datetime
from settings import DB_PATH

COLUMNS = [
    "record_id",
    "record_type",
    "name",
    "phone",
    "crop",
    "quantity_kg",
    "location",
    "date",
    "price_xof",
    "grade",
    "notes",
    "created_at",
]

def _ensure_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    if not os.path.exists(DB_PATH):
        pd.DataFrame(columns=COLUMNS).to_csv(DB_PATH, index=False)

def load_db():
    _ensure_db()
    df = pd.read_csv(DB_PATH)
    for c in COLUMNS:
        if c not in df.columns:
            df[c] = None
    return df[COLUMNS]

def add_record(rec):
    df = load_db()
    rec_out = {k: rec.get(k, None) for k in COLUMNS}
    rec_out["record_id"] = int(df["record_id"].max()) + 1 if len(df) and df["record_id"].notna().any() else 1
    rec_out["created_at"] = datetime.utcnow().isoformat()
    df = pd.concat([df, pd.DataFrame([rec_out])], ignore_index=True)
    df.to_csv(DB_PATH, index=False)

def delete_record(record_id: int):
    df = load_db()
    df = df[df["record_id"] != record_id]
    df.to_csv(DB_PATH, index=False)
