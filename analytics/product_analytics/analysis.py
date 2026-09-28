import pandas as pd
import numpy as np

def total_number_of_unitsSold(df:pd.DataFrame) -> dict:
    resut = int(df['units_sold'].sum())

    return {"Total_Units_Sold":resut}

def total_number_of_products(df:pd.DataFrame) -> dict:
    result = df['product_id'].nunique()
    return {"Total_Products":result}

def total_returned_units(df:pd.DataFrame) -> dict:
    result = int(df['returned_units'].sum())
    print(result)
    return {
        "Returned_Units": result
    }

def avg_product_price(df:pd.DataFrame) -> dict:
    result = int(df['price'].mean())
    print(result)
    return {
        "Avg_Product_Price": result
    }

def avg_product_cost(df:pd.DataFrame) -> dict:
    result = df['cost_price'].mean()
    return {
        "Avg_Product_Cost": result
    }
    
def gross_revenue(df:pd.DataFrame) -> dict:
    delivered_df = df[
        df['delivery_status'].isin(['Delivered', 'Delivered then Returned'])
    ]
    result =  int(delivered_df['item_revenue'].sum())
    return {"Gross_Revenue":result}

def net_revenue(df:pd.DataFrame) -> dict:
    revenue_df = df[
        df['delivery_status'].isin([
            'Delivered',
            'Delivered then Returned'
        ])
    ]
    gross_revenue = revenue_df['item_revenue'].sum()
    refund_amount = revenue_df['refund_amount'].sum()

    result = gross_revenue - refund_amount

    return {"Net_Revenue":result}

def get_product_sales_summary():
    pass

def total_revenue(df:pd.DataFrame) -> dict:
    delivered_df = df.loc[df['order_status'] == "Delivered",:]
    result =  int(delivered_df['item_revenue'].sum())
    return {"Total_Revenue":result}


def total_cost(df:pd.DataFrame) -> dict:
    delivered_df = df.loc[df['order_status'] == "Delivered",:]
    result = int(delivered_df['item_cost'].sum())
    return {"Total_cost":result}


def total_profit(df:pd.DataFrame) -> dict:
    delivered_df = df.loc[df['order_status'] == "Delivered",:]
    result= int(delivered_df['profit'].sum())
    return {"Total_Profit":result}

def profit_margin(df:pd.DataFrame) -> dict:
    delivered_df = df.loc[df['order_status'] == "Delivered",:]
    result = (
        delivered_df['profit'].sum() /
        delivered_df['item_revenue'].sum()
    ) * 100

    return {"Profit_Margin":result}

def total_number_of_returns(df:pd.DataFrame) -> dict:
    df_return = df.loc[df['return_status'] == 'Refund Completed',:]
    result = df_return.shape[0]
    return {"Total_Returns":result}

def product_return_rate(df:pd.DataFrame) -> dict:
    delivered = (
        df['delivery_status'] == 'Delivered'
    ).sum()

    delivered_then_returned = (
        df['delivery_status'] == 'Delivered then Returned'
    ).sum()

    result = (
        delivered_then_returned
        / (delivered + delivered_then_returned)
    ) * 100

    return {"Product return rate":result}


def top_10_products_sold(df: pd.DataFrame) -> list[dict]:
    result = (
        df.groupby('product_name')['units_sold']
        .sum()
        .reset_index()
        .sort_values('units_sold', ascending=False).head(10)
    )
 
    return result.to_dict(orient="records")


def top_10_which_category_sold(df: pd.DataFrame) -> list[dict]:
    result = (
        df.groupby('category')['units_sold']
        .sum()
        .reset_index()
        .sort_values('units_sold', ascending=False).head(10)
    )

    return result.to_dict(orient="records")


def price_vs_units_sold(df:pd.DataFrame) -> list[dict]:
    
    result = (
        df[['product_name', 'price', 'units_sold']]
        .sort_values('units_sold', ascending=False)
    )

    return result.to_dict(orient='records')

def top_10_revenue_generate_products(df: pd.DataFrame) -> list[dict]:
    df['revenue'] = df['price'] * df['units_sold']
    result = (
         df.groupby('product_name')
        .agg(
            revenue=('revenue', 'sum'),
            price=('price', 'first')
        )
        .reset_index()
        .sort_values('revenue', ascending=False)
        .head(10)
    )

    return result.to_dict(orient="records")

def top_10_revenue_generate_category(df: pd.DataFrame) -> list[dict]:
    df = df.loc[df["order_status"] == "Delivered", :]

    result = (
        df.groupby("category", as_index=False)["item_revenue"]
        .sum()
        .sort_values("item_revenue", ascending=False)
        .head(10)
    )

    result["revenue_contribution_pct"] = (
        result["item_revenue"] / df["item_revenue"].sum() * 100
    )

    return result.to_dict(orient="records")
    

def top_profit_products(df: pd.DataFrame) -> list[dict]:
    df = df.loc[df["order_status"] == "Delivered", :]

    result = (
        df.groupby("product_name", as_index=False)["profit"]
        .sum()
        .sort_values("profit", ascending=False)
        .head(10)
    )

    result["profit_contribution_pct"] = (
        result["profit"] / df["profit"].sum() * 100
    )

    return result.to_dict(orient="records")

def top_loss_products(df: pd.DataFrame) -> list[dict]:

    df = df.loc[df["order_status"] == "Delivered", :]

    result = (
        df.groupby("product_name")
        .agg(
            profit=("profit", "sum"),
            item_cost=("item_cost", "sum"),
            revenue=("item_revenue", "sum"),
            total_quantity=("quantity", "sum"),
            avg_unit_price=("unit_price", "mean"),
            avg_cost_price=("cost_price", "mean"),
            avg_discount_pct=("discount_percentage_item", "mean")
        )
    )

    result = result[result["profit"] < 0]

    result = (
        result
        .sort_values("profit")
        .head(10)
    )

    result["avg_profit_per_unit"] = (
        result["profit"] / result["total_quantity"]
    )

    result["profit_margin_pct"] = (
        result["profit"] / result["revenue"] * 100
    )

    result["avg_selling_price_after_discount"] = (
        result["avg_unit_price"]
        * (1 - result["avg_discount_pct"] / 100)
    )

    result = result.reset_index()

    return result.to_dict(orient="records")


def top_return_rate_products(df: pd.DataFrame) -> list[dict]:
    result = (
        df.groupby("product_name")
        .agg(
            total_orders=("product_name", "size"),
            avg_rating=("rating", "mean"),
            returned_orders=(
                "return_status",
                lambda x: (x == "Refund Completed").sum()
            ),
            most_common_sentiment=(
                "review_sentiment",
                lambda x: x.mode().iloc[0] if not x.mode().empty else None
            )
        )
        .reset_index()
    )

    result["return_rate_pct"] = (
        result["returned_orders"] / result["total_orders"] * 100
    )

    result = (
        result[result["total_orders"] >= 100]
        .sort_values("return_rate_pct", ascending=False)
        .head(10)
    )

    return result.to_dict(orient="records")


def monthly_trend_of_particular_product(df:pd.DataFrame,product_name:str) -> list[dict]:
    # product_name = "Kala-Vaidya Deluxe Laptop"

    result = df[
        df['product_name'] == product_name
    ].copy()

    result['year'] = result['order_date'].dt.year
    result['month'] = result['order_date'].dt.month

    result = (
        result
        .groupby(['year', 'month'])['item_revenue']
        .sum()
        .reset_index()
    )
    return result.to_dict(orient="records")


def product_performance(df: pd.DataFrame) -> list[dict]:
    result = (
        df.groupby("product_name", as_index=False)
        .agg(
            revenue=("item_revenue", "sum"),
            profit=("profit", "sum"),
            quantity_sold=("quantity", "sum")
        )
    )

    result["profit_margin_pct"] = (
        result["profit"] / result["revenue"] * 100
    )

    result = (
        result
        .sort_values("revenue", ascending=False)
        .head(10)
    )

    return result.to_dict(orient="records")
    

