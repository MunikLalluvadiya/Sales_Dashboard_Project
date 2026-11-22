CREATE TABLE IF NOT EXISTS Customers (
    Customer_ID   TEXT PRIMARY KEY,
    Customer_Name TEXT,
    City          TEXT,
    Region        TEXT
);

CREATE TABLE IF NOT EXISTS Products (
    Product_ID   TEXT PRIMARY KEY,
    Product_Name TEXT,
    Category     TEXT,
    Unit_Price   REAL
);

CREATE TABLE IF NOT EXISTS Sales (
    Order_ID      TEXT PRIMARY KEY,
    Order_Date    TEXT,
    Customer_ID   TEXT,
    Product_ID    TEXT,
    Quantity      INTEGER,
    Sales_Amount  REAL,
    Payment_Mode  TEXT,
    FOREIGN KEY (Customer_ID) REFERENCES Customers(Customer_ID),
    FOREIGN KEY (Product_ID)  REFERENCES Products(Product_ID)
);