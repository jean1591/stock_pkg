# FILES
from stock import OHLCV, Interval, Window, Indicators
from strategy import apply_strategy, p_ma_squeeze

# PACKAGES
from datetime import datetime


cryptos = ["BTC-USD", "ETH-USD", "MIOTA-USD"]
df_list = []
for crypto in cryptos:
  c_df = OHLCV.fetch(crypto, window=Window.TWO_YEARS, indicators=[Indicators.MA])
  df_list.append(apply_strategy(c_df, p_ma_squeeze))


print(f"REPORT: {datetime.now().strftime('%Y-%m-%d (%H:%M)')}")
for key, df in enumerate(df_list):
  print(f"{cryptos[key]}")
  print(df.tail())

  c_d_last_row = df.iloc[-1].to_dict()

  if c_d_last_row["order_type"] in ["buy", "sell"]:
    print(f"{c_d_last_row['order_type']} signal => {cryptos[key]}")
  
  print(f"\n\n{'=====' * 15}\n")