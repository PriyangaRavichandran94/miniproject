import streamlit as st
import pandas as pd
import sqlite3
import pydeck as pdk

def run():
    st.title("📍 Map with Location Pins")

    conn = sqlite3.connect("database/database.db")
    df = pd.read_sql("SELECT * FROM cleaned_listings", conn)
    conn.close()

    # Clean coordinates
    df["Latitude"] = pd.to_numeric(df["Latitude"], errors="coerce")
    df["Longitude"] = pd.to_numeric(df["Longitude"], errors="coerce")
    df = df.dropna(subset=["Latitude", "Longitude"])

    if df.empty:
        st.warning("No valid coordinates found")
        return

    # 📍 Add icon data
    df["icon_data"] = [{
        "url": "https://cdn-icons-png.flaticon.com/512/684/684908.png",  # pin icon
        "width": 125,
        "height": 125,
        "anchorY": 125
    }] * len(df)

    # 📍 Icon Layer (PIN)
    layer = pdk.Layer(
        type="IconLayer",
        data=df,
        get_icon="icon_data",
        get_position='[Longitude, Latitude]',
        get_size=2,
        size_scale=8,
        pickable=True
    )

    # View
    view_state = pdk.ViewState(
        latitude=df["Latitude"].mean(),
        longitude=df["Longitude"].mean(),
        zoom=10
    )

    # Tooltip
    tooltip = {
        "html": "<b>City:</b> {City} <br/> <b>Price:</b> {Price}",
        "style": {"backgroundColor": "black", "color": "white"}
    }

    st.pydeck_chart(pdk.Deck(
        layers=[layer],
        initial_view_state=view_state,
        tooltip=tooltip
    ))

     # BAR CHART
    st.subheader("Avg Price by City")
    st.bar_chart(df.groupby("City")["Price"].mean())

    # PIE (using pandas only)
    if "Property_Type" in df.columns:
        st.subheader("Property Type Distribution")
        st.write(df["Property_Type"].value_counts())

    # LINE CHART
    if "Date_Listed" in df.columns:
        df["Date_Listed"] = pd.to_datetime(df["Date_Listed"], errors="coerce")
        trend = df.groupby(df["Date_Listed"].dt.to_period("M")).size()
        st.subheader("Monthly Trend")
        st.line_chart(trend)

    # TABLE
    st.subheader("Data Table")
    st.dataframe(df)