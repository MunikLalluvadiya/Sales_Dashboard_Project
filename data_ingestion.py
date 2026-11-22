import sqlite3
import os
from src.data_cleaning import load_and_clean

df = load_and_clean()

if os.path.exists("database/sales.db"):
    os.remove("database/sales.db")


conn = sqlite3.connect("database/sales.db")
with open("sql/create_tables.sql") as f:
    conn.executescript(f.read())

    # table schema
    customers = df[["Customer_ID", "Customer_Name", "City", "Region"]].drop_duplicates()
    products  = df[["Product_ID", "Product_Name", "Category", "Unit_Price"]].drop_duplicates()
    sales     = df[["Order_ID", "Order_Date", "Customer_ID", "Product_ID",
                    "Quantity", "Sales_Amount", "Payment_Mode"]].copy()

    sales["Order_Date"] = sales["Order_Date"].dt.strftime("%Y-%m-%d")

    # create tables
    customers.to_sql("Customers", conn, if_exists="append", index=False)
    products.to_sql("Products", conn, if_exists="append", index=False)
    sales.to_sql("Sales", conn, if_exists="append", index=False)

    conn.commit()
    
    # for test
    for t in ["Customers", "Products", "Sales"]:
        print(t, conn.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0])

    conn.close()