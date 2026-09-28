import pandas as pd


month_order = {
    'January': 1,
    'February': 2,
    'March': 3,
    'April': 4,
    'May': 5,
    'June': 6,
    'July': 7,
    'August': 8,
    'September': 9,
    'October': 10,
    'November': 11,
    'December': 12
}

def total_customers_by_gender(df:pd.DataFrame) -> list[dict]:
    result = (
        df.groupby("gender")
        .agg(count=("customer_id","count"))
        .reset_index()
    )
    return result.to_dict(orient="records")

def get_customer_segment(df:pd.DataFrame) -> list[dict]:
    result = (
        df.groupby("customer_segment")
        .agg(count=("customer_id", "count"))
        .reset_index()
        .sort_values(by="count", ascending=False)
    )

    return result.to_dict(orient="records")

def get_avg_order_value(df:pd.DataFrame) -> dict:
    avg_order_value = df["average_order_value"].mean()
    return {'average_order_value':avg_order_value}

def get_avg_customer_spend(df:pd.DataFrame) -> dict:

    return {"average_customer_spend":df['total_spend'].mean()}

def get_total_customers(df:pd.DataFrame) -> dict:
    result = len(df)

    return {"total_customers": result}

def get_churn_rate(df:pd.DataFrame) -> dict:
    churned_df = df[df["customer_status"] == "Churned"]

    return {"churn_rate":(len(churned_df) / len(df)) * 100}

def get_monthly_signup_by_gender(df:pd.DataFrame) -> list[dict]:
    """
    get customer signup counts grouped by month and gender
    use this tool when the user asks  about gender wise signup trends
    """
    result = (
        df.groupby(
            ["customer_signup_month", "gender"]
        )
        .agg(count=("customer_id", "count"))
        .reset_index()
        .sort_values(by="count", ascending=False)
    )

    return result.to_dict(orient="records")

    


def get_monthly_signup_counts(df:pd.DataFrame) -> list[dict]:
    """
    Get the total number of customer signups for each month.
    Use this tool when the user asks about monthly signup counts,
    highest signup months, or lowest signup months.
    """
    result = (
        df.groupby("customer_signup_month")
        .agg(count=("customer_id", "count"))
        .reset_index()
        .sort_values(by="count", ascending=False)
    )

    return result.to_dict(orient="records")



def customer_signup_yearwise_trend(df:pd.DataFrame) -> list[dict]:
    """
    Analyze customer signup trends by year and month.

    This function counts the number of customer signups for each month
    within each signup year, orders the months chronologically, and
    returns the result in a tool-friendly dictionary format.

    Parameters
    ----------
    df : pd.DataFrame
        Customer dataset containing the following columns:
        - customer_id: Unique identifier of the customer.
        - customer_signup_year: Year in which the customer signed up.
        - customer_signup_month: Month in which the customer signed up.

    Returns
    -------
    dict
        Customer signup counts grouped by year and month.
        Each record contains:
        - customer_signup_year: Signup year.
        - month: Signup month.
        - count: Number of customers who signed up.
    """
    result = pd.pivot_table(
        df,
        index = "customer_signup_year",
        columns='customer_signup_month',
        values='customer_id',
        aggfunc='count',
        fill_value=0
    )

    result = result.reset_index()




    result = result.melt(
        id_vars='customer_signup_year',
        var_name='month',
        value_name='count'
    )

    result["month_num"] = (
        result['month'].map(month_order)
    )

    result = (
        result
        .sort_values(['customer_signup_year', 'month_num'])
        .drop(columns='month_num')
        .reset_index(drop=True)
    )

    return result.to_dict(orient="records")



def customer_churn_analysis(df:pd.DataFrame) -> list[dict]:
    """
    Analyze the distribution of customers by their status.

    Groups customers by customer status and counts the number of
    customers in each status category. The result can be used by
    other components for visualization or further analysis.

    Parameters
    ----------
    df : pd.DataFrame
        Customer dataset containing:
        - customer_id: Unique identifier of the customer.
        - customer_status: Current status of the customer,
          such as Active or Churned.

    Returns
    -------
    list[dict]
        Customer counts grouped by customer status.
        Each dictionary contains:
        - customer_status: Customer status category.
        - count: Number of customers in that status.
    """
    churn_anl = df.groupby('customer_status').agg(count = ("customer_id","count")).reset_index()

    return churn_anl.to_dict(orient="records")


def average_order_value_of_churned_customers(df: pd.DataFrame) -> list[dict]:
    """
    Calculate the average total spend of churned customers.

    Filters the customer dataset to include only churned customers
    and calculates their average total spend.

    Parameters
    ----------
    df : pd.DataFrame
        Customer dataset containing:
        - customer_status: Customer status used to identify churned customers.
        - total_spend: Total amount spent by each customer.

    Returns
    -------
    float
        Average total spend of churned customers.
    """

    churned_customers = df[df["customer_status"] == "Churned"]

    average_churned_order_value = churned_customers["total_spend"].mean()

    return average_churned_order_value.to_dict(orient="records")


def average_order_value_of_customer_status(df:pd.DataFrame) -> list[dict]:
    """
    Calculate the average order value for each customer status.

    Groups customers by their status and calculates the mean
    average order value for each status category.

    Parameters
    ----------
    df : pd.DataFrame
        Customer dataset containing:
        - customer_status: Customer status category.
        - average_order_value: Average order value associated
          with each customer.

    Returns
    -------
    list[dict]
        Average order value grouped by customer status.
        Each dictionary contains:
        - customer_status: Customer status category.
        - average_order_value: Mean average order value for that status.
    """
    result = df.groupby("customer_status").agg(
        average_order_value=("average_order_value", "mean")
    )

    return result.to_dict(orient="records")



def customer_status_rate(df: pd.DataFrame) -> list[dict]:
    """
    Calculate the percentage distribution of customers by status.

    Counts customers in each customer status category and calculates
    the percentage of total customers represented by each category.

    Parameters
    ----------
    df : pd.DataFrame
        Customer dataset containing:
        - customer_status: Status/category of each customer.

    Returns
    -------
    list[dict]
        Customer status percentages.
        Each dictionary contains:
        - customer_status: Customer status category.
        - percentage: Percentage of customers in that category.
    """

    result = (
        df["customer_status"]
        .value_counts(normalize=True)
        .mul(100)
        .rename_axis("customer_status")
        .reset_index(name="percentage")
    )

    return result.to_dict(orient="records")



def customer_segment_analysis(df: pd.DataFrame) -> list[dict]:
    """
    Analyze customer spending behavior across customer segments.

    Groups customers by customer segment and calculates spending
    statistics including mean, median, standard deviation, customer
    count, total spending, and coefficient of variation.

    Parameters
    ----------
    df : pd.DataFrame
        Customer dataset containing:
        - customer_segment: Customer segment/category.
        - total_spend: Total amount spent by each customer.
        - customer_id: Unique customer identifier.

    Returns
    -------
    list[dict]
        Customer segment-level spending analysis. Each dictionary
        contains:
        - customer_segment: Customer segment.
        - total_spend_mean: Mean customer spending.
        - total_spend_median: Median customer spending.
        - total_spend_std: Standard deviation of customer spending.
        - cust_count: Number of customers in the segment.
        - total_sum: Total spending of the segment.
        - cv: Coefficient of variation as a percentage.
    """

    result = df.groupby("customer_segment").agg(
        total_spend_mean=("total_spend", "mean"),
        total_spend_median=("total_spend", "median"),
        total_spend_std=("total_spend", "std"),
        cust_count=("customer_id", "count"),
        total_sum=("total_spend", "sum")
    ).reset_index()

    result["cv"] = (
        result["total_spend_std"] /
        result["total_spend_mean"]
    ) * 100

    return result.to_dict(orient="records")
