# FILES
from stock import OHLCV, Interval, Window, Indicators

ticker = "^FCHI"

cac_40 = OHLCV.fetch(crypto, window=Window.MAX, indicators=[Indicators.MA])
