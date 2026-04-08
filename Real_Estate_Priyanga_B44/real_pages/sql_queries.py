import streamlit as st
import pandas as pd
import sqlite3

def run():
    st.title("🧠 SQL Queries")

    conn = sqlite3.connect("database/database.db")

    queries = {

"Avg Price by City": """
SELECT City, AVG(Price) AS Avg_Price
FROM cleaned_listings
GROUP BY City;
""",



#What is the average price per square foot by property type?

"Price per Sqft": """
SELECT Property_Type, AVG(Price/Sqft) AS Price_Per_Sqft
FROM cleaned_listings
GROUP BY Property_Type;
""",

#How does furnishing status impact property prices?

"Furnishing Impact": """
SELECT pa.Furnishing_Status, AVG(l.Price)
FROM cleaned_listings l
JOIN property_attributes pa ON l.Listing_ID = pa.Listing_ID
GROUP BY pa.Furnishing_Status;
""",
#Do properties closer to metro stations command higher prices?
"Metro Distance Impact": """
SELECT 
CASE 
 WHEN Metro_Distance_Km < 2 THEN 'Near'
 WHEN Metro_Distance_Km < 5 THEN 'Medium'
 ELSE 'Far'
END AS Category,
AVG(l.Price)
FROM cleaned_listings l
JOIN property_attributes pa ON l.Listing_ID = pa.Listing_ID
GROUP BY Category;
""",
#Are rented properties priced differently from non-rented ones?
"Rented vs Non-Rented": """
SELECT pa.Is_Rented, AVG(l.Price)
FROM cleaned_listings l
JOIN property_attributes pa ON l.Listing_ID = pa.Listing_ID
GROUP BY pa.Is_Rented;
""",

#How do bedrooms and bathrooms affect pricing?
"Bedrooms Impact": """
SELECT Bedrooms, AVG(l.Price)
FROM cleaned_listings l
JOIN property_attributes pa ON l.Listing_ID = pa.Listing_ID
GROUP BY Bedrooms;
""",


#Do properties with parking and power backup sell at higher prices?
"Amenities Impact": """
SELECT Parking_Available, Power_Backup, AVG(l.Price)
FROM cleaned_listings l
JOIN property_attributes pa ON l.Listing_ID = pa.Listing_ID
GROUP BY Parking_Available, Power_Backup;
""",

#How does year built influence listing price?
"Year Built Impact": """
SELECT Year_Built, AVG(l.Price)
FROM cleaned_listings l
JOIN property_attributes pa ON l.Listing_ID = pa.Listing_ID
GROUP BY Year_Built;
""",

#Which cities have the highest median property prices?
"Median Price Cities": """
SELECT City, AVG(Price) AS Median_Price
FROM cleaned_listings
GROUP BY City
ORDER BY Median_Price DESC;
""",

#How are properties distributed across price buckets?
"Median Price Cities": """
SELECT City, AVG(Price) AS Median_Price
FROM cleaned_listings
GROUP BY City
ORDER BY Median_Price DESC;
""",

#What is the average days on market by city?
"Days on Market": """
SELECT l.City, AVG(s.Days_On_Market)
FROM sales_cleaned s
JOIN cleaned_listings l ON s.Listing_ID = l.Listing_ID
GROUP BY l.City;
""",
#Which property types sell the fastest?
"Fastest Sales": """
SELECT l.Property_Type, AVG(s.Days_On_Market)
FROM sales_cleaned s
JOIN cleaned_listings l ON s.Listing_ID = l.Listing_ID
GROUP BY l.Property_Type
ORDER BY AVG(s.Days_On_Market);
""",

#What percentage of properties are sold above listing price?
"Above Listing %": """
SELECT COUNT(*) * 100.0 / (SELECT COUNT(*) FROM sales)
FROM sales_cleaned s
JOIN cleaned_listings l ON s.Listing_ID = l.Listing_ID
WHERE s.Sale_Price > l.Price;
""",

#What is the sale-to-list price ratio by city?
"Sale/List Ratio": """
SELECT l.City, AVG(s.Sale_Price / l.Price)
FROM sales_cleaned s
JOIN cleaned_listings l ON s.Listing_ID = l.Listing_ID
GROUP BY l.City;
""",

#Which listings took more than 90 days to sell?
"Slow Listings": """
SELECT Listing_ID, Days_On_Market
FROM sales_cleaned
WHERE Days_On_Market > 90;
""",

#How does metro distance affect time on market?
"Metro vs Time": """
SELECT pa.Metro_Distance_Km, AVG(s.Days_On_Market)
FROM sales_cleaned s
JOIN property_attributes pa ON s.Listing_ID = pa.Listing_ID
GROUP BY pa.Metro_Distance_Km;
""",

#What is the monthly sales trend?
"Monthly Sales": """
SELECT strftime('%Y-%m', Sale_Date) AS Month, COUNT(*)
FROM sales_cleaned
GROUP BY Month;
""",

#Which properties are currently unsold?
"Unsold Properties": """
SELECT Listing_ID
FROM cleaned_listings
WHERE Listing_ID NOT IN (SELECT Listing_ID FROM sales_cleaned);
""",

#Which agents have closed the most sales?
"Top Agents": """
SELECT Name, Deals_Closed
FROM agents
ORDER BY Deals_Closed DESC;
""",
#Who are the top agents by total sales revenue?
"Agent Revenue": """
SELECT a.Name, SUM(s.Sale_Price)
FROM agents a
JOIN cleaned_listings l ON a.Agent_ID = l.Agent_ID
JOIN sales_cleaned s ON l.Listing_ID = s.Listing_ID
GROUP BY a.Name;
""",

#Which agents close deals fastest?
"Fastest Agents": """
SELECT Name, Avg_Closing_Days
FROM agents
ORDER BY Avg_Closing_Days;
""",

#Does experience correlate with deals closed?
"Experience vs Deals": """
SELECT Experience_Years, AVG(Deals_Closed)
FROM agents
GROUP BY Experience_Years;
""",

#Do agents with higher ratings close deals faster?
"Rating vs Speed": """
SELECT Rating, AVG(Avg_Closing_Days)
FROM agents
GROUP BY Rating;
""",

#What is the average commission earned by each agent?
"Commission": """
SELECT Name, Commission_Rate * Deals_Closed AS Estimated_Commission
FROM agents;
""",

#Which agents currently have the most active listings?
"Active Listings": """
SELECT a.Name, COUNT(l.Listing_ID)
FROM agents a
JOIN cleaned_listings l ON a.Agent_ID = l.Agent_ID
GROUP BY a.Name;
""",
#What percentage of buyers are investors vs end users?
"Buyer Type %": """
SELECT Buyer_Type, COUNT(*) * 100.0 / (SELECT COUNT(*) FROM buyers)
FROM buyers
GROUP BY Buyer_Type;
""",

#Which cities have the highest loan uptake rate?
"Loan Uptake": """
SELECT l.City,
COUNT(CASE WHEN b.Loan_Taken = 1 THEN 1 END) * 100.0 / COUNT(*)
FROM buyers b
JOIN sales_cleaned s ON b.Sale_ID = s.Listing_ID
JOIN cleaned_listings l ON s.Listing_ID = l.Listing_ID
GROUP BY l.City;
""",

#What is the average loan amount by buyer type?
"Avg Loan": """
SELECT Buyer_Type, AVG(Loan_Amount)
FROM buyers
GROUP BY Buyer_Type;
""",

#Which payment mode is most commonly used?
"Payment Mode": """
SELECT Payment_Mode, COUNT(*)
FROM buyers
GROUP BY Payment_Mode;
""",

#Do loan-backed purchases take longer to close?
"Loan vs Closing Time": """
SELECT b.Loan_Taken, AVG(s.Days_On_Market)
FROM buyers b
JOIN sales_cleaned s ON b.Sale_ID = s.Listing_ID
GROUP BY b.Loan_Taken;
"""
    }

    selected = st.selectbox("Select Query", list(queries.keys()))

    st.code(queries[selected])

    df = pd.read_sql(queries[selected], conn)

    st.dataframe(df)

    conn.close()