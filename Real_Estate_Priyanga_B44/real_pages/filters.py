import streamlit as st
import pandas as pd
import sqlite3

def get_data():
    conn = sqlite3.connect("database/database.db")
    df = pd.read_sql("SELECT * FROM cleaned_listings", conn)
    conn.close()
    return df

def run():
    st.title("🎛️ Filters Page")

    df = get_data()

    if df.empty:
        st.warning("No data available")
        return

    # City Multi-select
    cities = st.multiselect("City", df["City"].dropna().unique())

    # Property Type
    prop_type = st.selectbox(
        "Property Type",
        ["All"] + list(df["Property_Type"].dropna().unique())
    ) if "Property_Type" in df.columns else "All"

    # Price Slider
    min_price = int(df["Price"].min())
    max_price = int(df["Price"].max())
    price_range = st.slider("Price Range", min_price, max_price, (min_price, max_price))

    # Agent
    agent = st.selectbox(
        "Agent",
        ["All"] + list(df["Agent_Name"].dropna().unique())
    ) if "Agent_Name" in df.columns else "All"

    # Date Filter
    if "Listing_Date" in df.columns:
        df["Listing_Date"] = pd.to_datetime(df["Listing_Date"], errors="coerce")
        date_range = st.date_input("Date Range", [])
    else:
        date_range = []

    # Apply filters
    filtered = df.copy()

    if cities:
        filtered = filtered[filtered["City"].isin(cities)]

    if prop_type != "All":
        filtered = filtered[filtered["Property_Type"] == prop_type]

    filtered = filtered[
        filtered["Price"].between(price_range[0], price_range[1])
    ]

    if agent != "All":
        filtered = filtered[filtered["Agent_Name"] == agent]

    if len(date_range) == 2:
        filtered = filtered[
            (filtered["Listing_Date"] >= pd.to_datetime(date_range[0])) &
            (filtered["Listing_Date"] <= pd.to_datetime(date_range[1]))
        ]

    st.dataframe(filtered)