import streamlit as st
import filters
import visualizations
import crud
import sql_queries

st.set_page_config(layout="wide")
st.title("🏠 Real Estate Analytics")

page = st.sidebar.selectbox(
    "Navigation",
    ["Filters", "Visualizations", "CRUD", "SQL Queries"]
)

if page == "Filters":
    filters.run()
elif page == "Visualizations":
    visualizations.run()
elif page == "CRUD":
    crud.run()
elif page == "SQL Queries":
    sql_queries.run()