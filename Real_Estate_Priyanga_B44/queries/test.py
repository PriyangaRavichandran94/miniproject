import sqlite3
import pandas as pd

conn = sqlite3.connect("database/database.db")

df = pd.read_sql("""
SELECT count(*)
FROM cleaned_listings
""", conn)

print(df)

df1 = pd.read_sql("""
SELECT *
FROM cleaned_listings where  Listing_ID='L01179'
LIMIT 5
""", conn)

print(df1)

df2 = pd.read_sql("""
SELECT *
FROM buyers
LIMIT 5
""", conn)

print(df2)