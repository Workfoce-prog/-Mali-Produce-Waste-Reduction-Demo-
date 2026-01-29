from __future__ import annotations
import os
import pandas as pd
from datetime import datetime
from settings import DB_PATH

COLUMNS = [
    "record_id","record_type",
    "name","phone",
    "crop","quantity_kg",
    "location","date",
    "price_xof","grade","notes",
    "hub_name","storage_days","storage_fee_xof",
    "payment_ref","payment_status",
    "created_at"
]

def _ensure_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    if not os.path.exists(DB_PATH):
        pd.DataFrame(columns=COLUMNS).to_csv(DB_PATH, index=False)

def load_db() -> pd.DataFrame:
    _ensure_db()
    df = pd.read_csv(DB_PATH)
    for c in COLUMNS:
        if c not in df.columns:
            df[c] = None
    return df[COLUMNS]

def save_db(df: pd.DataFrame) -> None:
    _ensure_db()
    df[COLUMNS].to_csv(DB_PATH, index=False)

def next_id(df: pd.DataFrame) -> int:
    if df.empty or df["record_id"].isna().all():
        return 1
    try:
        return int(df["record_id"].max()) + 1
    except Exception:
        return len(df) + 1

def add_record(record: dict) -> int:
    df = load_db()
    rid = next_id(df)
    rec = {k: record.get(k, None) for k in COLUMNS}
    rec["record_id"] = rid
    rec["created_at"] = datetime.utcnow().isoformat()
    df = pd.concat([df, pd.DataFrame([rec])], ignore_index=True)
    save_db(df)
    return rid

def delete_record(record_id: int) -> None:
    df = load_db()
    df = df[df["record_id"] != record_id]
    save_db(df)
