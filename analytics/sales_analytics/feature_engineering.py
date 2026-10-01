import pandas as pd

def get_day_period(time):
    hour = pd.to_datetime(time).hour

    if 0 <= hour < 4:
        return "Midnight"
    elif 4 <= hour < 7:
        return "Early Morning"
    elif 7 <= hour < 12:
        return "Morning"
    elif 12 <= hour < 16:
        return "Afternoon"
    elif 16 <= hour < 20:
        return "Evening"
    else:
        return "Night"

def fe(df: pd.DataFrame):
    try:
        df = df.copy()

        df['order_date'] = pd.to_datetime(df['order_date'])

        df['year'] = df['order_date'].dt.year
        df['month'] = df['order_date'].dt.month_name()
        df['day'] = df['order_date'].dt.day_name()

        df['day_period'] = df['order_time'].apply(get_day_period)

        df.drop(
            columns=['order_time', 'order_date'],
            inplace=True
        )

        df.drop(
            columns=['order_item_id'],
            inplace=True
        )

        return df

    except Exception as e:
        raise RuntimeError(f"Feature engineering failed: {e}") from e

    