import pandas as pd

def get_monthly_revenue(df):
    monthly = df.groupby(df["Order_Date"].dt.to_period("M"))["Sales_Amount"].sum().reset_index()
    monthly["Order_Date"] = monthly["Order_Date"].dt.to_timestamp()
    monthly.columns = ["Month", "Revenue"]
    monthly["t"] = range(len(monthly))   # 0, 1, 2 ... = time index (the model's input)
    return monthly

def time_split(monthly, test_months=6):
    train = monthly.iloc[:-test_months]   # first 18 months
    test = monthly.iloc[-test_months:]    # last 6 months
    return train, test



import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error

def train_and_evaluate(train, test):
    model = LinearRegression()
    model.fit(train[["t"]], train["Revenue"])

    test = test.copy()
    test["Predicted"] = model.predict(test[["t"]])

    mae = mean_absolute_error(test["Revenue"], test["Predicted"])
    rmse = np.sqrt(mean_squared_error(test["Revenue"], test["Predicted"]))
    return test, mae, rmse

def forecast_next(monthly, months=3):
    model = LinearRegression()
    model.fit(monthly[["t"]], monthly["Revenue"])   # refit on all 24 months

    last_t = monthly["t"].iloc[-1]
    future = pd.DataFrame({"t": range(last_t + 1, last_t + 1 + months)})
    future["Month"] = pd.date_range(
        monthly["Month"].iloc[-1] + pd.offsets.MonthBegin(1), periods=months, freq="MS"
    )
    future["Predicted"] = model.predict(future[["t"]])
    return future