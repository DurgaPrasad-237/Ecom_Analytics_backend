import pandas as pd

def handle_return_status(final_df:pd.DataFrame):
    final_df.loc[
        final_df['return_status'].isna() &
        (final_df['order_status'] != 'Returned'),
        'return_status'
    ] = 'Not Returned'

    final_df.loc[
        final_df['return_status'].isna() &
        (final_df['order_status'] == 'Returned'),
        'return_status'
    ] = 'Unknown'

    return final_df


def change_dates_datatype(final_df:pd.DataFrame):
    final_df['order_date'] = pd.to_datetime(final_df['order_date'], errors='coerce')
    final_df['expected_delivery_date'] = pd.to_datetime(final_df['expected_delivery_date'], errors='coerce')
    final_df['actual_delivery_date'] = pd.to_datetime(final_df['actual_delivery_date'], errors='coerce')

    return final_df


