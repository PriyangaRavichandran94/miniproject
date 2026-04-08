import streamlit as st
import pandas as pd
import sqlite3

def run():
    st.title("🛠 CRUD Operations")

    conn = sqlite3.connect("database/database.db")

    table = st.selectbox("Select Table", ["cleaned_listings", "agents", "buyers"])

    df = pd.read_sql(f"SELECT * FROM {table}", conn)
    st.dataframe(df)

    columns = df.columns.tolist()

    # ADD
    st.subheader("Add Record")
    new_data = {}

    for col in columns:
        new_data[col] = st.text_input(f"{col}")

    if st.button("Insert"):
        placeholders = ",".join(["?"] * len(columns))
        conn.execute(
            f"INSERT INTO {table} VALUES ({placeholders})",
            list(new_data.values())
        )
        conn.commit()
        st.success("Inserted")

    # DELETE
    st.subheader("Delete Record")
    del_id = st.text_input("Enter ID")

    if st.button("Delete"):
        conn.execute(f"DELETE FROM {table} WHERE rowid=?", (del_id,))
        conn.commit()
        st.success("Deleted")

    # UPDATE
    st.subheader("Update Record")
    row_id = st.text_input("Row ID")
    col_name = st.selectbox("Column", columns)
    new_val = st.text_input("New Value")

    if st.button("Update"):
        conn.execute(
            f"UPDATE {table} SET {col_name}=? WHERE rowid=?",
            (new_val, row_id)
        )
        conn.commit()
        st.success("Updated")

    conn.close()