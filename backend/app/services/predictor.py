import datetime

import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression

from app.services.data_fetcher import get_historical_gold_prices

# How many calendar days of history to train on by default.
_DEFAULT_HISTORY_DAYS = 365


def train_model(df: pd.DataFrame) -> LinearRegression:
    """Fit a LinearRegression on historical gold price data.

    The feature is an integer ordinal (days since the first row) so the model
    learns a linear trend over time.  The target is the closing price.

    Args:
        df: DataFrame with columns ``date`` (datetime.date) and ``price`` (float),
            as returned by ``get_historical_gold_prices``.

    Returns:
        A fitted ``LinearRegression`` instance.

    Raises:
        ValueError: if *df* has fewer than 2 rows.
    """
    if len(df) < 2:
        raise ValueError(
            f"Need at least 2 data points to train, got {len(df)}."
        )

    origin = pd.Timestamp(df["date"].iloc[0])
    X = np.array(
        [(pd.Timestamp(d) - origin).days for d in df["date"]]
    ).reshape(-1, 1)
    y = df["price"].to_numpy()

    model = LinearRegression()
    model.fit(X, y)
    return model


def predict_future(days: int, history_days: int = _DEFAULT_HISTORY_DAYS) -> list[dict]:
    """Predict gold closing prices for the next *days* calendar days.

    Fetches recent history, trains a linear-trend model, then extrapolates
    forward starting from the day after the last known trading date.

    Args:
        days:         Number of future days to predict.
        history_days: How many historical trading days to train on.

    Returns:
        List of dicts, each with:
            ``date``            – ISO-8601 string (YYYY-MM-DD)
            ``predicted_price`` – float, predicted USD price per troy ounce
    """
    if days < 1:
        raise ValueError(f"days must be >= 1, got {days}.")

    df = get_historical_gold_prices(history_days)
    model = train_model(df)

    origin = pd.Timestamp(df["date"].iloc[0])
    last_date = pd.Timestamp(df["date"].iloc[-1])

    # Build ordinals for each of the next *days* calendar days.
    future_dates = [last_date + datetime.timedelta(days=i + 1) for i in range(days)]
    X_future = np.array(
        [(d - origin).days for d in future_dates]
    ).reshape(-1, 1)

    predictions = model.predict(X_future)

    return [
        {
            "date": d.strftime("%Y-%m-%d"),
            "predicted_price": round(float(p), 2),
        }
        for d, p in zip(future_dates, predictions)
    ]
