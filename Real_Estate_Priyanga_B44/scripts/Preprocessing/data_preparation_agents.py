import pandas as pd
import json

with open('dataset/raw/agents_cleaned.json') as f:
    data = json.load(f)

df = pd.json_normalize(data)

df['deals_closed'] = pd.to_numeric(df['deals_closed'], errors='coerce')
df['rating'] = pd.to_numeric(df['rating'], errors='coerce')
df['experience_years'] = pd.to_numeric(df['experience_years'], errors='coerce')

df.drop_duplicates(inplace=True)

df.to_csv('dataset/processed/agents.csv', index=False)