import pandas as pd 

def load_and_clean():
        
    df = pd.read_csv("dataset/sales_data.csv")

    # print(df.head())
    # print(df.tail())
    # print(df.describe())
    # print(df.info())

    # print(df.isnull().sum())

    df = df.drop_duplicates()
    df["Order_Date"] = pd.to_datetime(df["Order_Date"])
    df["Month"] = df["Order_Date"].dt.month
    df["Year"] = df["Order_Date"].dt.year

    # print(df.info())
    # # print(df.shape)

    return df

