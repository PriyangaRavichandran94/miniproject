import sqlite3

conn = sqlite3.connect('database/database.db')
cursor = conn.cursor()

# Listings
cursor.execute("""
CREATE TABLE cleaned_listings (
Listing_ID INTEGER PRIMARY KEY,
City TEXT,
Property_Type TEXT,
Price REAL,
Area_sqft REAL,
Agent_ID INTEGER,
Listed_Date DATE
)
""")

# Property Attributes
cursor.execute("""
CREATE TABLE property_attributes (
Listing_ID INTEGER,
Bedrooms INTEGER,
Bathrooms INTEGER,
Furnishing_Status TEXT,
Metro_Distance_Km REAL,
Parking_Available BOOLEAN,
FOREIGN KEY(Listing_ID) REFERENCES cleaned_listings(Listing_ID)
)
""")

# Agents
cursor.execute("""
CREATE TABLE agents (
Agent_ID INTEGER PRIMARY KEY,
Name TEXT,
Deals_Closed INTEGER,
Rating REAL
)
""")

# Sales
cursor.execute("""
CREATE TABLE sales_cleaned (
    Sale_ID INTEGER PRIMARY KEY AUTOINCREMENT,
    Listing_ID INTEGER,
    Sale_Date DATE,
    Sale_Price REAL,
    Days_On_Market INTEGER,
    FOREIGN KEY(Listing_ID) REFERENCES listings(Listing_ID)
)
""")

# Buyers
cursor.execute("""
CREATE TABLE buyers (
    Buyer_ID INTEGER PRIMARY KEY,
    Sale_ID INTEGER,
    Buyer_Type TEXT,
    Payment_Mode TEXT,
    Loan_Taken BOOLEAN,
    Loan_Provider TEXT,
    Loan_Amount REAL,
    FOREIGN KEY(Sale_ID) REFERENCES sales(Sale_ID)
)
""")

conn.commit()
conn.close()