import pandas as pd
import json


with open('dataset/listings_final_expanded.json', 'r') as file:
    data = json.load(file)


df = pd.DataFrame(data)


df = pd.json_normalize(data)


df.columns = df.columns.str.replace('.', '_')


df.fillna(0, inplace=True)


if 'Listed_Date' in df.columns:
    df['Listed_Date'] = pd.to_datetime(df['Listed_Date'])


if 'Price' in df.columns:
    df['Price'] = pd.to_numeric(df['Price'], errors='coerce')

if 'Area_sqft' in df.columns:
    df['Area_sqft'] = pd.to_numeric(df['Area_sqft'], errors='coerce')


if 'Is_Rented' in df.columns:
    df['Is_Rented'] = df['Is_Rented'].astype(bool)

df.drop_duplicates(inplace=True)


df.to_csv('dataset/cleaned_listings.csv', index=False)