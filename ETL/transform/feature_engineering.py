import pandas as pd


def convert_to_12_hour(time_value):
    """
    Convert 24-hour time into 12-hour AM/PM format.
    Example: 22:35:23 -> 10:35:23 PM
    """

    if pd.isna(time_value):
        return None

    time_value = str(time_value).strip()

    parsed_time = pd.to_datetime(
        time_value,
        format="%H:%M:%S",
        errors="coerce"
    )

    if pd.isna(parsed_time):
        return None

    return parsed_time.strftime("%I:%M:%S %p")


def get_hour(time_value):
    """
    Extract the hour from a 24-hour time value.
    """

    if pd.isna(time_value):
        return None

    parsed_time = pd.to_datetime(
        str(time_value).strip(),
        format="%H:%M:%S",
        errors="coerce"
    )

    if pd.isna(parsed_time):
        return None

    return parsed_time.hour


def classify_time(time_value):
    hour = get_hour(time_value)

    if hour is None:
        return "unknown"

    if 4 <= hour < 7:
        return "early_morning"
    elif 7 <= hour < 12:
        return "morning"
    elif 12 <= hour < 16:
        return "afternoon"
    elif 16 <= hour < 21:
        return "evening"
    elif 21 <= hour < 24:
        return "night"
    else:
        return "midnight"


def classify_time_range(time_value):
    hour = get_hour(time_value)

    if hour is None:
        return "unknown"

    if 4 <= hour < 7:
        return "04:00 AM - 07:00 AM"
    elif 7 <= hour < 12:
        return "07:00 AM - 12:00 PM"
    elif 12 <= hour < 16:
        return "12:00 PM - 04:00 PM"
    elif 16 <= hour < 21:
        return "04:00 PM - 09:00 PM"
    elif 21 <= hour < 24:
        return "09:00 PM - 12:00 AM"
    else:
        return "12:00 AM - 04:00 AM"


def orders_table(df_orders):
    """
    Create order-related feature columns.
    """

    # Convert order_date into datetime
    df_orders["order_date"] = pd.to_datetime(
        df_orders["order_date"],
        errors="coerce"
    )

    # Convert order_time from 24-hour format to 12-hour format
    df_orders["order_time"] = df_orders["order_time"].apply(
        convert_to_12_hour
    )

    # Create date features
    df_orders["order_month"] = (
        df_orders["order_date"].dt.month_name()
    )

    df_orders["order_year"] = (
        df_orders["order_date"].dt.year
    )

    # Create time features
    df_orders["time_category"] = (
        df_orders["order_time"].apply(classify_time)
    )

    df_orders["order_time_range"] = (
        df_orders["order_time"].apply(classify_time_range)
    )

    return df_orders


def customer_signup_month(df_customer):
    df_customer['customer_signup_date'] = pd.to_datetime(df_customer['customer_signup_date'])
    df_customer['customer_signup_month'] = df_customer['customer_signup_date'].dt.month_name()

    return df_customer

def customer_signup_year(df_customer):
    df_customer['customer_signup_date'] = pd.to_datetime(df_customer['customer_signup_date'])
    df_customer['customer_signup_year'] = df_customer['customer_signup_date'].dt.year

    return df_customer


def enrich_order_items_with_returns(order_items,returns):
    order_items = order_items.merge(
        returns[['order_id', 'product_id', 'return_status', 'refund_amount']],
        left_on=['order_id', 'product_id', 'item_revenue'],
        right_on=['order_id', 'product_id', 'refund_amount'],
        how='left'
    )

    order_items['refund_amount'] = order_items['refund_amount'].fillna(0)

    order_items = order_items.drop(columns=['return_status'])

    order_items = order_items.merge(
        returns[['order_id', 'product_id', 'refund_amount', 'return_status']],
        on=['order_id', 'product_id', 'refund_amount'],
        how='left'
    )

    order_items['return_status'] = order_items['return_status'].fillna('Not Returned')

    order_items = order_items.drop_duplicates(
        subset=['order_item_id']
    )

    return order_items


def calculate_returned_units_per_product(order_items,products):
    returned_products = (
        order_items[order_items['refund_amount'] > 0]
        .groupby('product_id')
        .agg(
            returned_units=('quantity', 'sum')
        )
        .sort_values('returned_units', ascending=False)
    )

    products = products.merge(
        returned_products,
        on='product_id',
        how='left'
    )
    products['returned_units'] = products['returned_units'].fillna(0).astype(int)
    return products

def calculate_units_sold_per_product(order_items, products):
    products_sold_units = (
        order_items
        .groupby('product_id')
        .agg(
            units_sold=('quantity', 'sum')
        )
        .sort_values(by='units_sold', ascending=False)
    )

    products = products.merge(
        products_sold_units,
        on='product_id',
        how='left'
    )

    return products

def calculate_product_return_rate(products):
    products['return_rate %'] = (products['returned_units']/products['units_sold'])*100
    return products