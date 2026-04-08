import pandas as pd
import json

with open('dataset/raw/property_attributes_final_expanded.json') as f:
    data = json.load(f)

df = pd.json_normalize(data)

df.columns = df.columns.str.replace('.', '_')


cols = ['bedrooms','bathrooms','floor_number','total_floors',
        'year_built','metro_distance_km','tenant_count']

for col in cols:
    df[col] = pd.to_numeric(df[col], errors='coerce')


bool_cols = ['is_rented','parking_available','power_backup']
for col in bool_cols:
    df[col] = df[col].astype(bool)

df.drop_duplicates(inplace=True)

df.to_csv('dataset/processed/property_attributes.csv', index=False)