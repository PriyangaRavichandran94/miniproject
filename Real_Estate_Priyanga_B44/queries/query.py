import sqlite3
import pandas as pd

conn = sqlite3.connect("database/database.db")

def run_query(title, query):
    print(f"\n📊 {title}")
    print("-" * 50)
    df = pd.read_sql(query, conn)
    print(df)

run_query("SELECT","SELECT * FROM cleaned_listings;")

#What is the average listing price by city?#
run_query("Avg Price by City", """
SELECT City, AVG(Price) AS Avg_Price
FROM cleaned_listings
GROUP BY City;
""")



#What is the average price per square foot by property type?

run_query("Price per Sqft", """
SELECT Property_Type, AVG(Price/Sqft) AS Price_Per_Sqft
FROM cleaned_listings
GROUP BY Property_Type;
""")

#How does furnishing status impact property prices?

run_query("Furnishing Impact", """
SELECT pa.Furnishing_Status, AVG(l.Price)
FROM cleaned_listings l
JOIN property_attributes pa ON l.Listing_ID = pa.Listing_ID
GROUP BY pa.Furnishing_Status;
""")

#Do properties closer to metro stations command higher prices?
run_query("Metro Distance Impact", """
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
""")
#Are rented properties priced differently from non-rented ones?
run_query("Rented vs Non-Rented", """
SELECT pa.Is_Rented, AVG(l.Price)
FROM cleaned_listings l
JOIN property_attributes pa ON l.Listing_ID = pa.Listing_ID
GROUP BY pa.Is_Rented;
""")

#How do bedrooms and bathrooms affect pricing?
run_query("Bedrooms Impact", """
SELECT Bedrooms, AVG(l.Price)
FROM cleaned_listings l
JOIN property_attributes pa ON l.Listing_ID = pa.Listing_ID
GROUP BY Bedrooms;
""")


#Do properties with parking and power backup sell at higher prices?
run_query("Amenities Impact", """
SELECT Parking_Available, Power_Backup, AVG(l.Price)
FROM cleaned_listings l
JOIN property_attributes pa ON l.Listing_ID = pa.Listing_ID
GROUP BY Parking_Available, Power_Backup;
""")

#How does year built influence listing price?
run_query("Year Built Impact", """
SELECT Year_Built, AVG(l.Price)
FROM cleaned_listings l
JOIN property_attributes pa ON l.Listing_ID = pa.Listing_ID
GROUP BY Year_Built;
""")

#Which cities have the highest median property prices?
run_query("Median Price Cities", """
SELECT City, AVG(Price) AS Median_Price
FROM cleaned_listings
GROUP BY City
ORDER BY Median_Price DESC;
""")

#How are properties distributed across price buckets?
run_query("Median Price Cities", """
SELECT City, AVG(Price) AS Median_Price
FROM cleaned_listings
GROUP BY City
ORDER BY Median_Price DESC;
""")

#What is the average days on market by city?
run_query("Days on Market", """
SELECT l.City, AVG(s.Days_On_Market)
FROM sales_cleaned s
JOIN cleaned_listings l ON s.Listing_ID = l.Listing_ID
GROUP BY l.City;
""")
#Which property types sell the fastest?
run_query("Fastest Sales", """
SELECT l.Property_Type, AVG(s.Days_On_Market)
FROM sales_cleaned s
JOIN cleaned_listings l ON s.Listing_ID = l.Listing_ID
GROUP BY l.Property_Type
ORDER BY AVG(s.Days_On_Market);
""")

#What percentage of properties are sold above listing price?
run_query("Above Listing %", """
SELECT COUNT(*) * 100.0 / (SELECT COUNT(*) FROM sales)
FROM sales_cleaned s
JOIN cleaned_listings l ON s.Listing_ID = l.Listing_ID
WHERE s.Sale_Price > l.Price;
""")

#What is the sale-to-list price ratio by city?
run_query("Sale/List Ratio", """
SELECT l.City, AVG(s.Sale_Price / l.Price)
FROM sales_cleaned s
JOIN cleaned_listings l ON s.Listing_ID = l.Listing_ID
GROUP BY l.City;
""")

#Which listings took more than 90 days to sell?
run_query("Slow Listings", """
SELECT Listing_ID, Days_On_Market
FROM sales_cleaned
WHERE Days_On_Market > 90;
""")

#How does metro distance affect time on market?
run_query("Metro vs Time", """
SELECT pa.Metro_Distance_Km, AVG(s.Days_On_Market)
FROM sales_cleaned s
JOIN property_attributes pa ON s.Listing_ID = pa.Listing_ID
GROUP BY pa.Metro_Distance_Km;
""")

#What is the monthly sales trend?
run_query("Monthly Sales", """
SELECT strftime('%Y-%m', Sale_Date) AS Month, COUNT(*)
FROM sales_cleaned
GROUP BY Month;
""")

#Which properties are currently unsold?
run_query("Unsold Properties", """
SELECT Listing_ID
FROM cleaned_listings
WHERE Listing_ID NOT IN (SELECT Listing_ID FROM sales_cleaned);
""")

#Which agents have closed the most sales?
run_query("Top Agents", """
SELECT Name, Deals_Closed
FROM agents
ORDER BY Deals_Closed DESC;
""")
#Who are the top agents by total sales revenue?
run_query("Agent Revenue", """
SELECT a.Name, SUM(s.Sale_Price)
FROM agents a
JOIN cleaned_listings l ON a.Agent_ID = l.Agent_ID
JOIN sales_cleaned s ON l.Listing_ID = s.Listing_ID
GROUP BY a.Name;
""")

#Which agents close deals fastest?
run_query("Fastest Agents", """
SELECT Name, Avg_Closing_Days
FROM agents
ORDER BY Avg_Closing_Days;
""")

#Does experience correlate with deals closed?
run_query("Experience vs Deals", """
SELECT Experience_Years, AVG(Deals_Closed)
FROM agents
GROUP BY Experience_Years;
""")

#Do agents with higher ratings close deals faster?
run_query("Rating vs Speed", """
SELECT Rating, AVG(Avg_Closing_Days)
FROM agents
GROUP BY Rating;
""")

#What is the average commission earned by each agent?
run_query("Commission", """
SELECT Name, Commission_Rate * Deals_Closed AS Estimated_Commission
FROM agents;
""")

#Which agents currently have the most active listings?
run_query("Active Listings", """
SELECT a.Name, COUNT(l.Listing_ID)
FROM agents a
JOIN cleaned_listings l ON a.Agent_ID = l.Agent_ID
GROUP BY a.Name;
""")
#What percentage of buyers are investors vs end users?
run_query("Buyer Type %", """
SELECT Buyer_Type, COUNT(*) * 100.0 / (SELECT COUNT(*) FROM buyers)
FROM buyers
GROUP BY Buyer_Type;
""")

#Which cities have the highest loan uptake rate?
run_query("Loan Uptake", """
SELECT l.City,
COUNT(CASE WHEN b.Loan_Taken = 1 THEN 1 END) * 100.0 / COUNT(*)
FROM buyers b
JOIN sales_cleaned s ON b.Sale_ID = s.Listing_ID
JOIN cleaned_listings l ON s.Listing_ID = l.Listing_ID
GROUP BY l.City;
""")

#What is the average loan amount by buyer type?
run_query("Avg Loan", """
SELECT Buyer_Type, AVG(Loan_Amount)
FROM buyers
GROUP BY Buyer_Type;
""")

#Which payment mode is most commonly used?
run_query("Payment Mode", """
SELECT Payment_Mode, COUNT(*)
FROM buyers
GROUP BY Payment_Mode;
""")

#Do loan-backed purchases take longer to close?
run_query("Loan vs Closing Time", """
SELECT b.Loan_Taken, AVG(s.Days_On_Market)
FROM buyers b
JOIN sales_cleaned s ON b.Sale_ID = s.Listing_ID
GROUP BY b.Loan_Taken;
""")



