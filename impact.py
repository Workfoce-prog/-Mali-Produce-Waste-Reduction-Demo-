import pandas as pd

def compute_impact(df: pd.DataFrame) -> dict:
    listings = df[df["record_type"] == "listing"].copy()
    total_supply = pd.to_numeric(listings["quantity_kg"], errors="coerce").fillna(0).sum()
    has_demand = (df["record_type"] == "demand").any()
    avoided = total_supply * (0.10 if has_demand else 0.0)

    avg_price = pd.to_numeric(listings["price_xof"], errors="coerce").fillna(0)
    avg_price = float(avg_price[avg_price > 0].mean()) if (avg_price > 0).any() else 400.0
    value = avoided * avg_price

    return {"avoided_waste_kg": float(avoided), "value_saved_xof": float(value)}
