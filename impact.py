import pandas as pd

def compute_impact(df: pd.DataFrame) -> dict:
    # A simple demo impact model:
    # - For each matched transaction: assume 10% waste avoided for that supply qty
    # - For each cold storage record: assume waste avoided increases with storage_days (capped)
    # - Value saved: avoided_waste_kg * avg_price_xof
    listings = df[df["record_type"] == "listing"].copy()
    demands = df[df["record_type"] == "demand"].copy()
    cold = df[df["record_type"] == "coldhub"].copy()

    # Approx. total listed supply
    total_supply = pd.to_numeric(listings["quantity_kg"], errors="coerce").fillna(0).sum()

    # Cold hub impact
    storage_qty = pd.to_numeric(cold["quantity_kg"], errors="coerce").fillna(0).sum()
    storage_days = pd.to_numeric(cold["storage_days"], errors="coerce").fillna(0)
    # avoided fraction based on storage days: 5% per day up to 25%
    avoided_frac = (storage_days * 0.05).clip(lower=0, upper=0.25).mean() if len(cold) else 0.0
    avoided_cold_kg = storage_qty * avoided_frac

    # Matching impact proxy: if there are both listings and demands, assume 10% of supply is rescued
    avoided_match_kg = total_supply * (0.10 if (len(listings) and len(demands)) else 0.0)

    avoided_total_kg = avoided_cold_kg + avoided_match_kg

    avg_price = pd.to_numeric(listings["price_xof"], errors="coerce").fillna(0)
    avg_price = float(avg_price[avg_price > 0].mean()) if (avg_price > 0).any() else 400.0

    value_saved_xof = avoided_total_kg * avg_price

    return {
        "total_supply_kg": float(total_supply),
        "cold_storage_qty_kg": float(storage_qty),
        "avoided_waste_kg": float(avoided_total_kg),
        "avg_price_xof_per_kg": float(avg_price),
        "value_saved_xof": float(value_saved_xof),
    }
