import pandas as pd
def periods(df:pd.DataFrame):
    df["year"] = df["order_date"].dt.year
    df["month"] = df["order_date"].dt.month
    df["day_of_week"] = df["order_date"].dt.dayofweek
    df["week_of_year"] = (
        df["order_date"].dt.isocalendar().week.astype(int)
    )
    df["quarter"] = df["order_date"].dt.quarter

    return df


def lag_features(df:pd.DataFrame):
    df["lag_1"] = (
        df.groupby("product_name")["quantity"].shift(1)
    )

    df["lag_7"] = (
        df.groupby("product_name")["quantity"].shift(7)
    )

    df["lag_14"] = (
        df.groupby("product_name")["quantity"].shift(14)
    )

    df["lag_28"] = (
        df.groupby("product_name")["quantity"].shift(28)
    )

    return df

def rolling_features(df:pd.DataFrame):
    # Previous 7-day average demand
    df["rolling_mean_7"] = (
        df.groupby("product_name")["quantity"]
        .transform(lambda x: x.shift(1).rolling(window=7).mean())
    )

    # Previous 14-day average demand
    df["rolling_mean_14"] = (
        df.groupby("product_name")["quantity"]
        .transform(lambda x: x.shift(1).rolling(window=14).mean())
    )

    # Previous 28-day average demand
    df["rolling_mean_28"] = (
        df.groupby("product_name")["quantity"]
        .transform(lambda x: x.shift(1).rolling(window=28).mean())
    )

    return df