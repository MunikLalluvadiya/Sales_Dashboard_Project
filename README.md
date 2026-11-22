Interactive Sales Dashboard & Revenue Forecasting System

A data analytics project that stores retail sales data in a SQL database, analyses it, shows it in an interactive Streamlit dashboard, and forecasts the next 3 months of revenue.

Made for the Data Analytics practical project, Baroda Institute of Technology, Bharuch.

1. Project Introduction

A retail company operates across multiple cities and regions and generates thousands of sales transactions every month, but has no central place to monitor performance. This project builds a dashboard that lets management track revenue, products, regions, customers and trends, and see a short-term revenue forecast.

2. Project Objectives
Import, clean and preprocess a sales dataset using Pandas and NumPy
Store the data in a related SQL database and query it with JOINs
Calculate business KPIs and perform Exploratory Data Analysis (EDA)
Build an interactive, database-connected dashboard with Streamlit and Plotly
Forecast the next 3 months of revenue using Linear Regression
Manage the project with Git and GitHub
3. Technologies Used
Technology	Purpose
Python	Programming
Pandas, NumPy	Data cleaning and calculations
SQLite (SQL)	Database
Matplotlib, Seaborn	EDA visualizations
Plotly	Interactive charts
Streamlit	Dashboard
Scikit-learn	Revenue forecasting
Git, GitHub	Version control
4. Dataset Description

The dataset is synthetic (generated for this project) and contains realistic retail sales for Jan 2024 to Dec 2025.

3,000 orders, 300 customers, 40 products in 5 categories
4 regions (North, South, East, West) and 12 cities
No missing values and no duplicate orders
Column	Description
Order_ID	Unique order identification
Order_Date	Date of transaction
Customer_ID, Customer_Name	Customer identification and name
Product_ID, Product_Name	Product identification and name
Category	Product category
Quantity	Units sold
Unit_Price	Price per unit
Sales_Amount	Quantity x Unit_Price
Region, City	Sales region and customer city
Payment_Mode	UPI, Credit Card, Debit Card, Cash, Net Banking
Database design (database/sales.db)

The CSV is split into 3 related tables:

Customers: Customer_ID (PK), Customer_Name, City, Region
Products: Product_ID (PK), Product_Name, Category, Unit_Price
Sales: Order_ID (PK), Order_Date, Customer_ID (FK), Product_ID (FK), Quantity, Sales_Amount, Payment_Mode

5. Project Structure
Sales_Dashboard_Project/
├── app.py                  # Streamlit dashboard
├── data_ingestion.py       # Loads the CSV into the SQL database
├── database/sales.db       # SQLite database
├── dataset/sales_data.csv  # Dataset
├── notebooks/sales_eda.ipynb   # EDA notebook
├── sql/
│   ├── create_tables.sql   # Table creation script
│   └── queries.sql         # Business queries
├── src/
│   ├── data_cleaning.py    # Data loading and cleaning
│   └── forecasting.py      # Revenue forecasting model
├── screenshots/
├── requirements.txt
└── README.md
6. Installation
Clone the repository:
git clone <your-repository-link>
cd Sales_Dashboard_Project
(Recommended) create and activate a virtual environment.
Install the packages:
pip install -r requirements.txt
7. How to Run the Project

Run all commands from the project root folder.

Build the database (creates database/sales.db from the CSV):
python data_ingestion.py
Start the dashboard:
streamlit run app.py
Open the EDA notebook: notebooks/sales_eda.ipynb
8. Dashboard Screenshots

KPIs and filters KPIs and filters

Sales performance Sales performance

Regional performance Regional performance

Product performance Product performance

Customer analysis Customer analysis

Revenue forecasting Revenue forecasting

9. Key Business Insights
Total revenue is about ₹30.56 million from 3,000 orders and 300 customers. The average order value is about ₹10,186.
West is the top region (about ₹12.69M, around 42% of revenue). East is the lowest (about ₹3.64M). Mumbai and Ahmedabad are the top cities.
Furniture is the best category (about ₹7.08M), followed closely by Electronics.
Treadmill, Sofa Set and Tablet earn the most revenue, while cheap items like Skipping Rope and Water Bottle sell the most units.
October, November and December are the strongest months (festive season).
Revenue grew about 19.2% from 2024 to 2025.
UPI is the most used payment mode (about 39% of orders).
Sales amount depends mainly on unit price (correlation about 0.88), not on quantity.
Most orders are low value, and a smaller number of high-value orders (furniture, electronics) contribute a large share of revenue.
10. Revenue Forecasting Results
Method: monthly revenue is aggregated, split by time (first 18 months for training, last 6 months for testing), and a Linear Regression model is trained on the time index.
Evaluation on the test period: MAE is about ₹293,884 and RMSE is about ₹330,495.
Forecast (Jan to Mar 2026): about ₹1.64M, ₹1.67M and ₹1.70M.
Limitation: the model captures the overall growth trend but not the seasonal peaks in Oct to Dec, so it under-predicts the festive months. A seasonal model would improve this.

Note: The forecast is an estimate based on historical data and is not a guaranteed business outcome.

11. Author

<Your Name>, IT Diploma Student GitHub: <your-github-link>
