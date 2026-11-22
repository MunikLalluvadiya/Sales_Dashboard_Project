
-- Query 1: Total sales by region
SELECT c.Region, SUM(s.Sales_Amount) AS Total_Sales
FROM Sales s
INNER JOIN Customers c ON s.Customer_ID = c.Customer_ID
GROUP BY c.Region
ORDER BY Total_Sales DESC;

-- Query 2: Top 10 selling products (by revenue)
SELECT p.Product_Name, SUM(s.Sales_Amount) AS Total_Sales, SUM(s.Quantity) AS Units_Sold
FROM Sales s
INNER JOIN Products p ON s.Product_ID = p.Product_ID
GROUP BY p.Product_ID, p.Product_Name
ORDER BY Total_Sales DESC
LIMIT 10;

-- Query 3: Monthly revenue
SELECT strftime('%Y-%m', Order_Date) AS Month, SUM(Sales_Amount) AS Revenue
FROM Sales
GROUP BY Month
ORDER BY Month;

-- Query 4: Customers with the highest purchases (top 10)
SELECT c.Customer_ID, c.Customer_Name, SUM(s.Sales_Amount) AS Total_Purchase
FROM Sales s
INNER JOIN Customers c ON s.Customer_ID = c.Customer_ID
GROUP BY c.Customer_ID, c.Customer_Name
ORDER BY Total_Purchase DESC
LIMIT 10;

-- Query 5: Category-wise sales
SELECT p.Category, SUM(s.Sales_Amount) AS Total_Sales
FROM Sales s
INNER JOIN Products p ON s.Product_ID = p.Product_ID
GROUP BY p.Category
ORDER BY Total_Sales DESC;

-- Query 6: Number of orders in each city
SELECT c.City, COUNT(s.Order_ID) AS Total_Orders
FROM Sales s
INNER JOIN Customers c ON s.Customer_ID = c.Customer_ID
GROUP BY c.City
ORDER BY Total_Orders DESC;

-- Query 7: Customer and sales information using JOIN (INNER JOIN)
SELECT s.Order_ID, s.Order_Date, c.Customer_Name, c.City,
       p.Product_Name, p.Category, s.Quantity, s.Sales_Amount
FROM Sales s
INNER JOIN Customers c ON s.Customer_ID = c.Customer_ID
INNER JOIN Products p  ON s.Product_ID  = p.Product_ID
ORDER BY s.Order_Date
LIMIT 20;

-- Query 8: LEFT JOIN - all customers, including those with no orders
SELECT c.Customer_ID, c.Customer_Name, COUNT(s.Order_ID) AS Total_Orders
FROM Customers c
LEFT JOIN Sales s ON c.Customer_ID = s.Customer_ID
GROUP BY c.Customer_ID, c.Customer_Name
ORDER BY Total_Orders ASC
LIMIT 10;

-- Query 9: RIGHT JOIN - all products, including those never sold
-- (RIGHT JOIN needs SQLite 3.39 or newer)
SELECT p.Product_Name, COUNT(s.Order_ID) AS Total_Orders
FROM Sales s
RIGHT JOIN Products p ON s.Product_ID = p.Product_ID
GROUP BY p.Product_ID, p.Product_Name
ORDER BY Total_Orders ASC
LIMIT 10;