import streamlit as st
import pandas as pd
from datetime import date

from settings import APP_TITLE, DEFAULT_LANGUAGE
from db import load_db, add_record, delete_record
from matching import match_supply_demand
from impact import compute_impact
from i18n import I18N

st.set_page_config(page_title=APP_TITLE, layout="wide")
st.title(APP_TITLE)

def t(key):
    lang = st.session_state.get("lang", DEFAULT_LANGUAGE)
    return I18N.get(key, {}).get(lang, I18N.get(key, {}).get("EN", key))

# Sidebar language toggle
st.sidebar.selectbox("Language", ["EN", "FR", "BM"], key="lang")

df = load_db()

tabs = st.tabs([
    t("TAB_LISTINGS"),
    t("TAB_DEMANDS"),
    t("TAB_MATCHING"),
    t("TAB_IMPACT"),
])

# ---------------- Listings (Farmers) ----------------
with tabs[0]:
    st.subheader(t("TAB_LISTINGS"))

    with st.form("listing_form", clear_on_submit=True):
        c1, c2, c3 = st.columns(3)
        name = c1.text_input("Farmer name")
        phone = c2.text_input("Phone")
        harvest_date = c3.date_input("Harvest date", value=date.today())

        c4, c5, c6, c7 = st.columns(4)
        crop = c4.text_input("Crop", "Tomato")
        quantity = c5.number_input("Quantity (kg)", min_value=1, value=100)
        location = c6.text_input("Location", "Sikasso")
        price = c7.number_input("Target price (XOF/kg)", min_value=0, value=350)

        notes = st.text_input("Notes (optional)", "")

        if st.form_submit_button(t("ADD")):
            add_record({
                "record_type": "listing",
                "name": name,
                "phone": phone,
                "crop": crop,
                "quantity_kg": quantity,
                "location": location,
                "date": str(harvest_date),
                "price_xof": price,
                "notes": notes,
            })
            st.success("Listing added.")
            st.rerun()

    df = load_db()
    listings = df[df["record_type"] == "listing"].copy()
    st.dataframe(listings, use_container_width=True)

# ---------------- Demands (Buyers) ----------------
with tabs[1]:
    st.subheader(t("TAB_DEMANDS"))

    with st.form("demand_form", clear_on_submit=True):
        c1, c2, c3 = st.columns(3)
        buyer = c1.text_input("Buyer name")
        phone = c2.text_input("Phone")
        delivery_date = c3.date_input("Delivery date", value=date.today())

        c4, c5, c6, c7 = st.columns(4)
        crop = c4.text_input("Crop", "Tomato")
        quantity = c5.number_input("Quantity needed (kg)", min_value=1, value=200)
        location = c6.text_input("Delivery location", "Bamako")
        offer = c7.number_input("Offer price (XOF/kg)", min_value=0, value=400)

        notes = st.text_input("Notes (optional)", "")

        if st.form_submit_button(t("ADD")):
            add_record({
                "record_type": "demand",
                "name": buyer,
                "phone": phone,
                "crop": crop,
                "quantity_kg": quantity,
                "location": location,
                "date": str(delivery_date),
                "price_xof": offer,
                "notes": notes,
            })
            st.success("Demand added.")
            st.rerun()

    df = load_db()
    demands = df[df["record_type"] == "demand"].copy()
    st.dataframe(demands, use_container_width=True)

# ---------------- Matching ----------------
with tabs[2]:
    st.subheader(t("TAB_MATCHING"))
    df = load_db()
    listings = df[df["record_type"] == "listing"].copy()
    demands = df[df["record_type"] == "demand"].copy()

    matches = match_supply_demand(listings, demands)
    if matches.empty:
        st.info("Add at least one listing and one demand to see matches.")
    else:
        st.dataframe(matches, use_container_width=True)

# ---------------- Impact ----------------
with tabs[3]:
    st.subheader(t("TAB_IMPACT"))
    df = load_db()
    metrics = compute_impact(df)

    c1, c2 = st.columns(2)
    c1.metric("Avoided waste (kg)", f"{metrics['avoided_waste_kg']:.0f}")
    c2.metric("Value saved (XOF)", f"{metrics['value_saved_xof']:.0f}")

    st.caption("Demo impact math. Replace with real baseline later.")
