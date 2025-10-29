-- Customer Purchase Insights (E-commerce) - SQL script
-- Author: Omar Aly

-- Assumes a table 'customer_purchases' with columns:
-- CustomerID (INT), PurchaseDate (DATE), Product (TEXT), Category (TEXT),
-- Amount (NUMERIC), PaymentMethod (TEXT), Country (TEXT)

-- DATA CLEANING & PREPARATION
-- 1. Quick look at data
SELECT * FROM customer_purchases LIMIT 10;

-- 2. Check for NULL or empty Amounts
SELECT COUNT(*) AS missing_amounts FROM customer_purchases WHERE Amount IS NULL OR Amount = '';

-- 3. Replace empty PaymentMethod/Country with 'Unknown'
UPDATE customer_purchases SET PaymentMethod = 'Unknown' WHERE PaymentMethod IS NULL OR PaymentMethod = '';
UPDATE customer_purchases SET Country = 'Unknown' WHERE Country IS NULL OR Country = '';

-- 4. Remove rows with missing or non-positive Amounts
DELETE FROM customer_purchases WHERE Amount IS NULL OR Amount = '' OR CAST(Amount AS REAL) <= 0;

-- 5. Trim whitespace from Product names (syntax may vary by SQL dialect)
-- Example for SQLite: UPDATE customer_purchases SET Product = TRIM(Product);

-- ANALYTICAL QUERIES

-- Query 1: Total sales per country
SELECT Country, ROUND(SUM(CAST(Amount AS REAL)),2) AS total_sales, COUNT(*) AS orders_count
FROM customer_purchases
GROUP BY Country
ORDER BY total_sales DESC;

-- Query 2: Top 10 products by revenue
SELECT Product, Category, ROUND(SUM(CAST(Amount AS REAL)),2) AS revenue, COUNT(*) AS units_sold
FROM customer_purchases
GROUP BY Product, Category
ORDER BY revenue DESC
LIMIT 10;

-- Query 3: Monthly sales pivot by category (using CASE WHEN for portability)
SELECT STRFTIME('%Y-%m', PurchaseDate) AS month,
       ROUND(SUM(CASE WHEN Category = 'Electronics' THEN CAST(Amount AS REAL) ELSE 0 END),2) AS Electronics,
       ROUND(SUM(CASE WHEN Category = 'Clothing' THEN CAST(Amount AS REAL) ELSE 0 END),2) AS Clothing,
       ROUND(SUM(CASE WHEN Category = 'Home' THEN CAST(Amount AS REAL) ELSE 0 END),2) AS Home,
       ROUND(SUM(CASE WHEN Category = 'Books' THEN CAST(Amount AS REAL) ELSE 0 END),2) AS Books,
       ROUND(SUM(CASE WHEN Category = 'Accessories' THEN CAST(Amount AS REAL) ELSE 0 END),2) AS Accessories,
       ROUND(SUM(CASE WHEN Category = 'Sports' THEN CAST(Amount AS REAL) ELSE 0 END),2) AS Sports
FROM customer_purchases
GROUP BY month
ORDER BY month;

-- Query 4: Average order value by customer
SELECT CustomerID, ROUND(AVG(CAST(Amount AS REAL)),2) AS avg_order_value, COUNT(*) AS orders_count
FROM customer_purchases
GROUP BY CustomerID
ORDER BY avg_order_value DESC
LIMIT 10;

-- Query 5: Sales by payment method
SELECT PaymentMethod, ROUND(SUM(CAST(Amount AS REAL)),2) AS total_sales, COUNT(*) AS orders_count
FROM customer_purchases
GROUP BY PaymentMethod
ORDER BY total_sales DESC;

-- Query 6: Top 5 customers by total spending
SELECT CustomerID, ROUND(SUM(CAST(Amount AS REAL)),2) AS total_spent, COUNT(*) AS orders_count
FROM customer_purchases
GROUP BY CustomerID
ORDER BY total_spent DESC
LIMIT 5;

-- Query 7: Top 3 categories per month (example of category trend)
SELECT STRFTIME('%Y-%m', PurchaseDate) AS month, Category, ROUND(SUM(CAST(Amount AS REAL)),2) AS category_sales
FROM customer_purchases
GROUP BY month, Category
ORDER BY month, category_sales DESC;
