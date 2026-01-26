import pandas as pd

def match_supply_demand(listings: pd.DataFrame, demands: pd.DataFrame) -> pd.DataFrame:
    if listings.empty or demands.empty:
        return pd.DataFrame()

    l = listings.copy()
    d = demands.copy()

    l["crop_norm"] = l["crop"].astype(str).str.strip().str.lower()
    d["crop_norm"] = d["crop"].astype(str).str.strip().str.lower()
    l["loc_norm"] = l["location"].astype(str).str.strip().str.lower()
    d["loc_norm"] = d["location"].astype(str).str.strip().str.lower()

    rows = []
    for _, dd in d.iterrows():
        subset = l[l["crop_norm"] == dd["crop_norm"]].copy()
        if subset.empty:
            continue

        subset["same_location"] = (subset["loc_norm"] == dd["loc_norm"]).astype(int)
        try:
            subset["qty_distance"] = (subset["quantity_kg"].astype(float) - float(dd["quantity_kg"])).abs()
        except Exception:
            subset["qty_distance"] = 999999

        # Score: location bonus + closeness
        subset["score"] = subset["same_location"] * 100 - subset["qty_distance"]
        subset = subset.sort_values("score", ascending=False).head(10)

        for _, ss in subset.iterrows():
            rows.append({
                "demand_id": int(dd["record_id"]),
                "buyer": dd["name"],
                "crop": dd["crop"],
                "demand_qty_kg": dd["quantity_kg"],
                "demand_location": dd["location"],
                "listing_id": int(ss["record_id"]),
                "farmer": ss["name"],
                "supply_qty_kg": ss["quantity_kg"],
                "supply_location": ss["location"],
                "price_xof": ss.get("price_xof", None),
                "grade": ss.get("grade", None),
                "match_score": round(float(ss["score"]), 2)
            })

    return pd.DataFrame(rows)
