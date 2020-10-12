# STOCK_PCK

A simple Yahoo Finance API wrapper that uses pandas and talib.


## Details
The wrapper will fetch data from the Yahoo Finance API and return a `pandas.DataFrame`. You can specify indicators to be added to the returned `DataFrame`

As of `2020-10-12`, the Intervals, Windows and Indicators are as follow:

### Intervals
`['MINUTE', 'TWO_MINUTE', 'FIVE_MINUTE', 'FIFTEEN_MINUTE', 'THIRTY_MINUTE', 'HOUR', 'DAY', 'FIVE_DAY', 'WEEK', 'MONTH', 'THREE_MONTH']`

### Windows
`['DAY', 'FIVE_DAYS', 'MONTH', 'QUARTER', 'HALF_YEAR', 'YEAR', 'TWO_YEARS', 'FIVE_YEARS', 'TEN_YEARS', 'YTD', 'MAX']`

### Indicators
`['ADX', 'BBANDS', 'EMA', 'MA', 'OBV', 'P_CHANGE', 'PSAR', 'RSI']`


## Usage
### Basic Usage
Fetching Apple OHLCV data on a one year window with daily data
Key | Value
--- | ---
Stock | `AAPL`
Interval | `DAY`
Window | `YEAR`
Indicators | `[]`

```python
from pkg_name import OHLCV
aapl_df = OHLCV.fetch("AAPL")
```

Results:
```python
              open    high     low   close    volume
date                                                
2019-10-10   56.98   57.61   56.83   57.52  113013.6
2019-10-11   58.24   59.41   58.08   59.05  166795.6
2019-10-14   58.72   59.53   58.67   58.97   96427.6
2019-10-15   59.10   59.41   58.72   58.83   87360.0
2019-10-16   58.34   58.81   58.30   58.59   73903.2
...            ...     ...     ...     ...       ...
2020-10-05  113.91  116.65  113.55  116.50  106243.8
2020-10-06  115.70  116.12  112.25  113.16  161498.2
2020-10-07  114.62  115.55  114.13  115.08   96849.0
2020-10-08  116.25  116.40  114.59  114.97   83477.2
2020-10-09  115.28  117.00  114.92  116.97   99893.4
```

### Specifying Interval & Window
Fetching Apple OHLCV data on a ten years window with weekly data
Key | Value
--- | ---
Stock | `AAPL`
Interval | `WEEK`
Window | `TEN_YEARS`
Indicators | `[]`

```python
from pkg_name import OHLCV, Interval, Window
aapl_df = OHLCV.fetch("AAPL", interval=Interval.WEEK, window=Window.TEN_YEARS)
```

Results:
```python
              open    high     low   close      volume
date                                                  
2010-10-11   10.53   11.25   10.45   11.24  2973880.00
2010-10-18   11.37   11.39   10.72   10.98  3971657.20
2010-10-25   11.04   11.13   10.75   10.75  2165956.80
2010-11-01   10.79   11.44   10.79   11.33  2369908.80
2010-11-08   11.33   11.48   10.84   11.00  2206660.40
...            ...     ...     ...     ...         ...
2020-09-14  114.72  118.83  106.09  106.84   944587.00
2020-09-21  104.54  112.86  103.10  112.28   847212.60
2020-09-28  115.01  117.72  112.22  113.02   640562.20
2020-10-05  113.91  117.00  112.25  116.97   547961.60
2020-10-09  115.28  117.00  114.92  116.97   100506.86
```

### Specifying Indicators
Fetching Apple OHLCV data on a ten years window with weekly data and MA and BBANDS indicators
Key | Value
--- | ---
Stock | `AAPL`
Interval | `WEEK`
Window | `TEN_YEARS`
Indicators | `[MA, BBANDS]`

```python
from pkg_name import OHLCV, Interval, Window, Indicators
aapl_df = OHLCV.fetch("AAPL", interval=Interval.WEEK, window=Window.TEN_YEARS, indicators=[Indicators.MA, Indicators.BBANDS])
```

Results:
```python
              open    high     low   close      volume    ma_5   ma_10   ma_20  ma_30  ma_50  ma_100  ma_200  u_band  m_band  l_band  p_band  p_band_ma_5
date                                                                                                                                                     
2010-10-11   10.53   11.25   10.45   11.24  2973880.00     NaN     NaN     NaN    NaN    NaN     NaN     NaN     NaN     NaN     NaN     NaN          NaN
2010-10-18   11.37   11.39   10.72   10.98  3971657.20     NaN     NaN     NaN    NaN    NaN     NaN     NaN     NaN     NaN     NaN     NaN          NaN
2010-10-25   11.04   11.13   10.75   10.75  2165956.80     NaN     NaN     NaN    NaN    NaN     NaN     NaN     NaN     NaN     NaN     NaN          NaN
2010-11-01   10.79   11.44   10.79   11.33  2369908.80     NaN     NaN     NaN    NaN    NaN     NaN     NaN     NaN     NaN     NaN     NaN          NaN
2010-11-08   11.33   11.48   10.84   11.00  2206660.40   11.06     NaN     NaN    NaN    NaN     NaN     NaN   11.47   11.06   10.65    7.14          NaN
...            ...     ...     ...     ...         ...     ...     ...     ...    ...    ...     ...     ...     ...     ...     ...     ...          ...
2020-09-14  114.72  118.83  106.09  106.84   944587.00  117.80  111.02   97.71  87.49  80.78   64.13   52.69  132.11  117.80  103.48   21.67        21.68
2020-09-21  104.54  112.86  103.10  112.28   847212.60  115.38  112.62   99.45  88.95  81.84   64.71   53.11  128.46  115.38  102.29   20.37        19.35
2020-09-28  115.01  117.72  112.22  113.02   640562.20  113.02  114.66  101.25  90.31  82.92   65.32   53.54  122.09  113.02  103.95   14.86        17.86
2020-10-05  113.91  117.00  112.25  116.97   547961.60  112.22  115.73  103.12  91.89  84.03   65.98   53.98  118.68  112.22  105.76   10.89        16.72
2020-10-09  115.28  117.00  114.92  116.97   100506.86  113.22  116.31  104.99  93.88  85.09   66.67   54.42  120.69  113.22  105.75   12.38        16.03
```

### Example with cryptos
Key | Value
--- | ---
Stock | `BTC-USD`
Interval | `MINUTE`
Window | `FIVE_DAYS`
Indicators | `[MA, BBANDS]`

```python
from pkg_name import OHLCV, Interval, Window, Indicators
btc_usd_df = OHLCV.fetch("BTC-USD", interval=Interval.MINUTE, window=Window.FIVE_DAYS, indicators=[Indicators.MA])
```

Results:
```python
                         open      high       low     close   volume      ma_5     ma_10     ma_20     ma_30     ma_50    ma_100    ma_200
date                                                                                                                                      
2020-10-07 23:01:00  10658.62  10658.62  10658.62  10658.62     0.00       NaN       NaN       NaN       NaN       NaN       NaN       NaN
2020-10-07 23:02:00  10658.49  10658.49  10658.49  10658.49  3125.25       NaN       NaN       NaN       NaN       NaN       NaN       NaN
2020-10-07 23:03:00  10658.58  10658.58  10658.58  10658.58   970.75       NaN       NaN       NaN       NaN       NaN       NaN       NaN
2020-10-07 23:04:00  10658.68  10658.68  10658.68  10658.68   421.89       NaN       NaN       NaN       NaN       NaN       NaN       NaN
2020-10-07 23:06:00  10658.37  10658.37  10658.37  10658.37     0.00  10658.55       NaN       NaN       NaN       NaN       NaN       NaN
...                       ...       ...       ...       ...      ...       ...       ...       ...       ...       ...       ...       ...
2020-10-12 10:22:00  11354.83  11354.83  11354.83  11354.83     0.00  11357.02  11356.99  11354.26  11349.42  11346.94  11356.75  11368.62
2020-10-12 10:23:00  11354.87  11354.87  11354.87  11354.87     0.00  11356.09  11357.07  11354.55  11350.43  11347.05  11356.40  11368.63
2020-10-12 10:24:00  11354.87  11354.87  11354.87  11354.87    61.44  11355.16  11357.14  11354.85  11351.43  11347.15  11356.05  11368.64
2020-10-12 10:25:00  11344.89  11344.89  11344.89  11344.89     0.00  11352.87  11355.89  11354.54  11351.79  11347.12  11355.62  11368.55
2020-10-12 10:26:23  11343.10  11343.10  11343.10  11343.10     0.00  11350.51  11354.24  11354.17  11351.83  11347.07  11355.18  11368.45
```