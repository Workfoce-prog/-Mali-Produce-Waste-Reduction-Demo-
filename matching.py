import pandas as pd

GRADE_WEIGHT = {"A": 30, "B": 15, "C": 0}

def match_supply_demand(listings: pd.DataFrame, demands: pd.DataFrame) -> pd.DataFrame:
    if listings.empty or demands.empty:
        return pd.DataFrame()

    l = listings.copy()
    d = demands.copy()

    l["crop_norm"] = l["crop"].astype(str).str.strip().str.lower()
    d["crop_norm"] = d["crop"].astype(str).str.strip().str.lower()
    l["loc_norm"] = l["location"].astype(str).str.strip().str.lower()
    d["loc_norm"] = d["location"].astype(str).str.strip().str.lower()

    l["grade_norm"] = l["grade"].astype(str).str.strip().str.upper()
    l["grade_score"] = l["grade_norm"].map(GRADE_WEIGHT).fillna(0).astype(float)

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

        subset["score"] = subset["grade_score"] + subset["same_location"] * 20 - subset["qty_distance"]
        subset = subset.sort_values("score", ascending=False).head(10)

        for _, ss in subset.iterrows():
            rows.append({
                "buyer": dd.get("name",""),
                "buyer_phone": dd.get("phone",""),
                "crop": dd.get("crop",""),
                "demand_qty_kg": dd.get("quantity_kg",""),
                "demand_location": dd.get("location",""),
                "farmer": ss.get("name",""),
                "farmer_phone": ss.get("phone",""),
                "supply_qty_kg": ss.get("quantity_kg",""),
                "supply_location": ss.get("location",""),
                "grade": ss.get("grade",""),
                "price_xof": ss.get("price_xof",""),
                "match_score": round(float(ss.get("score",0)), 2)
            })

    return pd.DataFrame(rows)
