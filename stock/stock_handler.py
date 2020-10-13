import requests
import pandas as pd
from datetime import datetime
from enum import Enum
from talib import ADX, BBANDS, EMA, MA, OBV, RSI, SAR


class Window(Enum):
    """Defines the possible historical time ranges to be fetched."""
    DAY = "1d"
    FIVE_DAYS = "5d"
    MONTH = "1mo"
    QUARTER = "3mo"
    HALF_YEAR = "6mo"
    YEAR = "1y"
    TWO_YEARS = "2y"
    FIVE_YEARS = "5y"
    TEN_YEARS = "10y"
    YTD = "ytd"
    MAX = "max"


class Interval(Enum):
    """Defines the possible lengths of each candle (OHLC) period."""
    MINUTE = "1m"
    TWO_MINUTE = "2m"
    FIVE_MINUTE = "5m"
    FIFTEEN_MINUTE = "15m"
    THIRTY_MINUTE = "30m"
    HOUR = "1h"
    DAY = "1d"
    FIVE_DAY = "5d"
    WEEK = "1wk"
    MONTH = "1mo"
    THREE_MONTH = "3mo"


class Indicators(Enum):
    ADX = "adx"
    BBANDS = ["u_band", "m_band", "l_band"]
    EMA = ["ema_5", "ema_10", "ema_20",
           "ema_30", "ema_50", "ema_100", "ema_200"]
    MA = ["ma_5", "ma_10", "ma_20", "ma_30", "ma_50", "ma_100", "ma_200"]
    OBV = "obv"
    P_CHANGE = ["p_change 1", "p_change 5", "p_change 20"]
    PSAR = "psar"
    RSI = "rsi"


class OHLCV:
    @ classmethod
    def help(self):
        print("Available Intervale Range:")
        print([e.name for e in Interval])

        print("Available Window Range:")
        print([e.name for e in Window])

        print("Available Indicators:")
        print([e.name for e in Indicators])

    @classmethod
    def fetch(self, symbol: str, interval: Interval = Interval.DAY, window: Window = Window.YEAR, indicators: Indicators = [], verbose=False) -> pd.DataFrame:
        """
        Fetch symbol stock OHLCV from Yahoo Finance API

        Args:
            symbol (str): Symbol to fetch
            interval (Interval, optional): Interval (hour, day, week, ...) of data. Defaults to Interval.DAY.
            window (Window, optional): Length (day, week, month, year) of interval. Defaults to Window.YEAR.
            indicators (Indicators, optional): Array of indicators to include in the result. Defaults to empty array.

        Returns:
            pd.DataFrame: OHLCV pandas DataFrame with interval on window length and indicators if specified
        """
        try:
            if verbose:
                print(
                    f"Fetching OHLCV {symbol} stock data on {interval.name} interval and {window.name} window")

            # Generic url to fetch
            url = f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}?region=FR&lang=fr-FR&includePrePost=false&interval={interval.value}&range={window.value}&corsDomain=fr.finance.yahoo.com&.tsrc=finance"

            req = requests.get(url)

            # Testing request status code
            if req.status_code == 200:

                # Extracting data as json
                data = req.json()

                # Creating new DataFrame
                df = pd.DataFrame()

                # Extract date from object
                if interval in [Interval.MINUTE, Interval.TWO_MINUTE, Interval.FIVE_MINUTE, Interval.FIFTEEN_MINUTE, Interval.THIRTY_MINUTE, Interval.HOUR]:
                    dateFromUnix = [datetime.utcfromtimestamp(dt).strftime(
                        "%Y-%m-%d %H:%M:%S") for dt in data["chart"]["result"][0]["timestamp"]]
                else:
                    dateFromUnix = [datetime.utcfromtimestamp(dt).strftime(
                        "%Y-%m-%d") for dt in data["chart"]["result"][0]["timestamp"]]

                # Date & OHLCV to DataFrame
                df["date"] = pd.to_datetime(dateFromUnix)
                df["open"] = data["chart"]["result"][0]["indicators"]["quote"][0]["open"]
                df["high"] = data["chart"]["result"][0]["indicators"]["quote"][0]["high"]
                df["low"] = data["chart"]["result"][0]["indicators"]["quote"][0]["low"]
                df["close"] = data["chart"]["result"][0]["indicators"]["quote"][0]["close"]
                df["volume"] = data["chart"]["result"][0]["indicators"]["quote"][0]["volume"]

                # Drop NaN on close col
                df.dropna(subset=["close"], inplace=True)

                # Divide volume column by a 1 000
                df["volume"] = df["volume"].div(1000)

                # Set date column as index
                df.set_index("date", inplace=True)

                for indicator in indicators:
                    # ADX
                    if indicator == Indicators.ADX:
                        df[indicator.value] = ADX(
                            df["high"], df["low"], df["close"])
                    # BBANDS
                    elif indicator == Indicators.BBANDS:
                        df[Indicators.BBANDS.value[0]], df[Indicators.BBANDS.value[1]
                                                           ], df[Indicators.BBANDS.value[2]] = BBANDS(df["close"])
                        df["p_band"] = 100 - \
                            (df["l_band"] / df["u_band"] * 100)
                        df["p_band_ma_5"] = MA(
                            df["p_band"], timeperiod=5)
                    # EMA
                    elif indicator == Indicators.EMA:
                        for ema in Indicators.EMA.value:
                            df[ema] = EMA(
                                df["close"], timeperiod=int(ema.split("_")[1]))
                    # MA
                    elif indicator == Indicators.MA:
                        for ma in Indicators.MA.value:
                            df[ma] = MA(
                                df["close"], timeperiod=int(ma.split("_")[1]))
    
                    # OBV
                    elif indicator == Indicators.OBV:
                        df[indicator.value] = OBV(df["close"], df["volume"])
                        df[indicator.value] = df[indicator.value].div(1000)
                    # PSAR
                    elif indicator == Indicators.PSAR:
                        df[indicator.value] = SAR(df["high"], df["low"])
                    # PERCENT CHANGE
                    elif indicator == Indicators.P_CHANGE:
                        for p_change in Indicators.P_CHANGE.value:
                            df[p_change] = df["close"].pct_change(
                                int(p_change.split(" ")[1])) * 100
                    # RSI
                    elif indicator == Indicators.RSI:
                        df[indicator.value] = RSI(df["close"])

                return df.round(decimals=2)

        except Exception as e:
            print(e)
