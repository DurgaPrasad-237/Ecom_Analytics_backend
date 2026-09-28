import pandas as pd


def handle_missing_values(
    df_customer,
    df_customer_reviews,
    df_orders,
    df_products,
    df_shipments
):
    # -------------------------
    # Customer
    # -------------------------

    # Age → fill missing with median
    df_customer["age"] = df_customer["age"].fillna(
        df_customer["age"].median()
    )

    # Preferred device → Unknown
    df_customer["preferred_device"] = (
        df_customer["preferred_device"].fillna("Unknown")
    )

    # Last order date → keep NULL


    # -------------------------
    # Customer Reviews
    # -------------------------

    # Review sentiment → Unknown
    df_customer_reviews["review_sentiment"] = (
        df_customer_reviews["review_sentiment"].fillna("Unknown")
    )

    invalid_ratings = df_customer_reviews.loc[
        ~df_customer_reviews["rating"].between(1, 5) |
        df_customer_reviews["rating"].isna(),
        "rating"
    ]

    if len(invalid_ratings) > 0:

        # Convert invalid ratings to missing
        df_customer_reviews.loc[
            ~df_customer_reviews["rating"].between(1, 5),
            "rating"
        ] = pd.NA

        # Find the most common valid rating for each product
        product_rating_mode = (
            df_customer_reviews.groupby("product_id")["rating"]
            .agg(lambda x: x.mode().iloc[0] if not x.mode().empty else pd.NA)
        )

        # Fill missing ratings using the product's mode
        df_customer_reviews["rating"] = (
            df_customer_reviews["rating"]
            .fillna(df_customer_reviews["product_id"].map(product_rating_mode))
        )




    # -------------------------
    # Orders
    # -------------------------

    # Coupon code:
    # NULL + discount = 0 → No Coupon
    # NULL + discount > 0 → Unknown

    no_coupon = (
        df_orders["coupon_code"].isna()
        & (df_orders["discount_percentage"] == 0)
    )

    unknown_coupon = (
        df_orders["coupon_code"].isna()
        & (df_orders["discount_percentage"] > 0)
    )

    df_orders.loc[no_coupon, "coupon_code"] = "No Coupon"
    df_orders.loc[unknown_coupon, "coupon_code"] = "Unknown"

    # Campaign ID → keep NULL


    # -------------------------
    # Products
    # -------------------------

    # Rating average → fill missing with median
    df_products["rating_average"] = df_products["rating_average"].fillna(
        df_products["rating_average"].median()
    )


    # -------------------------
    # Shipments
    # -------------------------

    # actual_delivery_date → keep NULL
    # delivery_days → keep NULL


    return (
        df_customer,
        df_customer_reviews,
        df_orders,
        df_products,
        df_shipments
    )


def remove_duplicates():
    pass

    

def fix_data_types(
    df_customer,
    df_customer_reviews,
    df_orders,
    df_products,
    df_shipments
):
    # ========== customer reviews ===============
    df_customer_reviews["review_date"] = pd.to_datetime(df_customer_reviews["review_date"])
    # ===========================================


    # ============== customers ===================
    df_customer['age'] = df_customer['age'].astype('Int64')
    df_customer['customer_signup_date'] = pd.to_datetime(df_customer["customer_signup_date"])
    df_customer['last_order_date'] = pd.to_datetime(df_customer["last_order_date"])
    # ==============================================


    # =============== orders ========================
    df_orders['order_date'] = pd.to_datetime(df_orders['order_date'])
    # ===============================================


    # ============= shipments ===============
    df_shipments['dispatch_date'] = pd.to_datetime(df_shipments['dispatch_date'])
    df_shipments['expected_delivery_date'] = pd.to_datetime(df_shipments['expected_delivery_date'])
    df_shipments['actual_delivery_date'] = pd.to_datetime(df_shipments['actual_delivery_date'])
    df_shipments['delivery_days'] = df_shipments['delivery_days'].astype('Int64')


    return (
    df_customer,
    df_customer_reviews,
    df_orders,
    df_products,
    df_shipments
    )


def validate_data_ranges():
    pass