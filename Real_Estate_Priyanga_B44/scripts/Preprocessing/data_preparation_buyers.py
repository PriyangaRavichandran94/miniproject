import pandas as pd
import json

with open('dataset/raw/buyers_cleaned.json') as f:
    data = json.load(f)

df = pd.json_normalize(data)

df['loan_amount'] = pd.to_numeric(df['loan_amount'], errors='coerce')
df['loan_taken'] = df['loan_taken'].astype(bool)

df.drop_duplicates(inplace=True)

df.to_csv('dataset/processed/buyers.csv', index=False)