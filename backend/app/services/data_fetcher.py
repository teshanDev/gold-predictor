import datetime

import httpx
import pandas as pd

# Yahoo Finance chart endpoint for COMEX gold futures (GC=F)
_GOLD_URL = "https://query1.finance.yahoo.com/v8/finance/chart/GC=F"
_HEADERS = {"User-Agent": "Mozilla/5.0"}


def get_current_gold_price() -> float:
    """Return the current gold spot price in USD per troy ounce.

    Source: Yahoo Finance (GC=F — COMEX gold front-month futures).
    Raises RuntimeError if the price cannot be retrieved.
    """
    try:
        with httpx.Client(timeout=10.0) as client:
            response = client.get(_GOLD_URL, headers=_HEADERS)
            response.raise_for_status()

        data = response.json()
        price = data["chart"]["result"][0]["meta"]["regularMarketPrice"]
        return float(price)

    except httpx.TimeoutException:
        raise RuntimeError("Request timed out while fetching gold price.")
    except httpx.HTTPStatusError as exc:
        raise RuntimeError(
            f"HTTP {exc.response.status_code} error from Yahoo Finance."
        )
    except (KeyError, IndexError, TypeError) as exc:
        raise RuntimeError(
            f"Unexpected response structure from Yahoo Finance: {exc}"
        )
    except httpx.RequestError as exc:
        raise RuntimeError(f"Network error while fetching gold price: {exc}")


def get_historical_gold_prices(days: int) -> pd.DataFrame:
    """Return the last *days* trading days of gold prices as a DataFrame.

    Columns:
        date  — datetime.date, the trading day
        price — float, closing price in USD per troy ounce (GC=F)

    Raises RuntimeError if data cannot be retrieved or parsed.
    """
    end = datetime.datetime.utcnow()
    # Add a calendar buffer so weekends/holidays don't reduce the row count.
    start = end - datetime.timedelta(days=days + 14)

    params = {
        "period1": int(start.timestamp()),
        "period2": int(end.timestamp()),
        "interval": "1d",
    }

    try:
        with httpx.Client(timeout=10.0) as client:
            response = client.get(_GOLD_URL, headers=_HEADERS, params=params)
            response.raise_for_status()

        data = response.json()
        result = data["chart"]["result"][0]
        timestamps = result["timestamp"]
        closes = result["indicators"]["quote"][0]["close"]

        df = pd.DataFrame({
            "date": pd.to_datetime(timestamps, unit="s").date,
            "price": pd.array(closes, dtype="Float64"),
        })
        df = df.dropna(subset=["price"]).tail(days).reset_index(drop=True)
        df["price"] = df["price"].astype(float)
        return df

    except httpx.TimeoutException:
        raise RuntimeError("Request timed out while fetching gold price history.")
    except httpx.HTTPStatusError as exc:
        raise RuntimeError(
            f"HTTP {exc.response.status_code} error from Yahoo Finance."
        )
    except (KeyError, IndexError, TypeError) as exc:
        raise RuntimeError(
            f"Unexpected response structure from Yahoo Finance: {exc}"
        )
    except httpx.RequestError as exc:
        raise RuntimeError(f"Network error while fetching gold price history: {exc}")
