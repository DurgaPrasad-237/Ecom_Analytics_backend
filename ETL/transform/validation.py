import pandas as pd


def validate_required_columns(df, required_columns, table_name):
    missing_columns = [
        column for column in required_columns
        if column not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            f"{table_name}: Missing columns: {missing_columns}"
        )


def validate_duplicate_keys(df, key_column, table_name):
    duplicate_count = df[key_column].duplicated().sum()

    if duplicate_count > 0:
        raise ValueError(
            f"{table_name}: {duplicate_count} duplicate "
            f"{key_column} values found"
        )


def validate_non_negative(df, columns, table_name):
    for column in columns:
        if (df[column] < 0).any():
            raise ValueError(
                f"{table_name}: Negative values found in {column}"
            )


def validate_foreign_key(
    child_df,
    child_column,
    parent_df,
    parent_column,
    relationship_name
):
    invalid_values = (
        ~child_df[child_column].isin(parent_df[parent_column])
    )

    if invalid_values.any():
        raise ValueError(
            f"{relationship_name}: Invalid foreign-key values found"
        )


def validate_date_columns(df, date_columns, table_name):
    for column in date_columns:
        if not pd.api.types.is_datetime64_any_dtype(df[column]):
            raise TypeError(
                f"{table_name}: {column} is not datetime type"
            )


def validate_data(
    df_customer,
    df_customer_review,
    df_orders,
    df_order_items,
    df_products,
    df_payments,
    df_returns,
    df_shipments
):
    # Required columns
    validate_required_columns(
        df_customer,
        ["customer_id"],
        "customers"
    )

    validate_required_columns(
        df_orders,
        ["order_id", "customer_id"],
        "orders"
    )

    validate_required_columns(
        df_order_items,
        ["order_item_id", "order_id", "product_id"],
        "order_items"
    )

    validate_required_columns(
        df_products,
        ["product_id"],
        "products"
    )

    validate_required_columns(
        df_shipments,
        ["shipment_id", "order_id"],
        "shipments"
    )

    # Duplicate primary keys
    validate_duplicate_keys(
        df_customer, "customer_id", "customers"
    )

    validate_duplicate_keys(
        df_orders, "order_id", "orders"
    )

    validate_duplicate_keys(
        df_order_items, "order_item_id", "order_items"
    )

    validate_duplicate_keys(
        df_products, "product_id", "products"
    )

    validate_duplicate_keys(
        df_shipments, "shipment_id", "shipments"
    )

    # Non-negative values
    validate_non_negative(
        df_order_items,
        ["quantity", "unit_price", "discount_percentage",
         "item_revenue", "item_cost"],
        "order_items"
    )

    validate_non_negative(
        df_shipments,
        ["delivery_days"],
        "shipments"
    )

    # Foreign keys
    validate_foreign_key(
        df_orders,
        "customer_id",
        df_customer,
        "customer_id",
        "orders → customers"
    )

    validate_foreign_key(
        df_order_items,
        "order_id",
        df_orders,
        "order_id",
        "order_items → orders"
    )

    validate_foreign_key(
        df_order_items,
        "product_id",
        df_products,
        "product_id",
        "order_items → products"
    )

    validate_foreign_key(
        df_shipments,
        "order_id",
        df_orders,
        "order_id",
        "shipments → orders"
    )

    # Date columns
    validate_date_columns(
        df_orders,
        ["order_date"],
        "orders"
    )

    validate_date_columns(
        df_shipments,
        [
            "dispatch_date",
            "expected_delivery_date",
            "actual_delivery_date"
        ],
        "shipments"
    )

    print("All validation checks passed successfully.")