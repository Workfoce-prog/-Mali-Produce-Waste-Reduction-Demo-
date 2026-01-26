
import streamlit as st
import pandas as pd
from datetime import date

from utils.settings import APP_TITLE, DEFAULT_LANGUAGE
from utils.db import load_db, add_record
from utils.matching import match_supply_demand
from utils.impact import compute_impact
from utils.i18n import I18N

st.set_page_config(page_title=APP_TITLE, layout="wide")
st.title(APP_TITLE)

# Language helper
def t(key):
    lang = st.session_state.get("lang", DEFAULT_LANGUAGE)
    return I18N.get(key, {}).get(lang, I18N.get(key, {}).get("EN", key))

st.sidebar.selectbox("Language", ["EN", "FR", "BM"], key="lang")

df = load_db()

tabs = st.tabs([
    t("TAB_LISTINGS"),
    t("TAB_DEMANDS"),
    t("TAB_MATCHING"),
    t("TAB_IMPACT")
])

with tabs[0]:
    st.subheader(t("TAB_LISTINGS"))
    with st.form("listing"):
        name = st.text_input("Farmer")
        crop = st.text_input("Crop", "Tomato")
        qty = st.number_input("Quantity (kg)", 1, 10000, 100)
        loc = st.text_input("Location", "Sikasso")
        if st.form_submit_button(t("ADD")):
            add_record({
                "record_type":"listing",
                "name":name,
                "crop":crop,
                "quantity_kg":qty,
                "location":loc,
                "date":str(date.today())
            })
            st.success("Added")
            st.rerun()
    st.dataframe(df[df.record_type=="listing"])

with tabs[1]:
    st.subheader(t("TAB_DEMANDS"))
    with st.form("demand"):
        name = st.text_input("Buyer")
        crop = st.text_input("Crop", "Tomato")
        qty = st.number_input("Needed (kg)", 1, 10000, 200)
        loc = st.text_input("Delivery location", "Bamako")
        if st.form_submit_button(t("ADD")):
            add_record({
                "record_type":"demand",
                "name":name,
                "crop":crop,
                "quantity_kg":qty,
                "location":loc,
                "date":str(date.today())
            })
            st.success("Added")
            st.rerun()
    st.dataframe(df[df.record_type=="demand"])

with tabs[2]:
    st.subheader(t("TAB_MATCHING"))
    listings = df[df.record_type=="listing"]
    demands = df[df.record_type=="demand"]
    matches = match_supply_demand(listings, demands)
    st.dataframe(matches)

with tabs[3]:
    st.subheader(t("TAB_IMPACT"))
    metrics = compute_impact(df)
    st.metric("Avoided waste (kg)", f"{metrics['avoided_waste_kg']:.0f}")
    st.metric("Value saved (XOF)", f"{metrics['value_saved_xof']:.0f}")
