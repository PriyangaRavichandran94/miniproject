import pandas as pd
import sqlite3

conn = sqlite3.connect('database/database.db')

files = ['cleaned_listings','property_attributes','agents']

for file in files:
    df = pd.read_csv(f'dataset/processed/{file}.csv')
    df.to_sql(file, conn, if_exists='replace', index=False)


sales_df = pd.read_csv("dataset/processed/sales_cleaned.csv")
sales_df.to_sql('sales_cleaned', conn, if_exists='append', index=False)


#Load buyers csv to database and assign the saleID values ad foreign key
buyers_df = pd.read_csv("dataset/processed/buyers.csv")
sales_df = pd.read_sql("SELECT Sale_ID FROM sales_cleaned", conn)
buyers_df['Sale_ID'] = sales_df['Sale_ID']
buyers_df.to_sql('buyers', conn, if_exists='append', index=False)

conn.close()