# FILES
from utils import get_stock
from stock import Window, Indicators


cryptos = ["BTC-USD", "ETH-USD", "MIOTA-USD"]
df_list = []
for crypto in cryptos:
  df_list.append(get_stock(crypto, window=Window.HALF_YEAR, indicators=[Indicators.MA]))


for key, df in enumerate(df_list):
  c_d_last_row = df.iloc[-1].to_dict()

  if c_d_last_row["order_type"] in ["buy", "sell"]:
    print(f"Send {c_d_last_row['order_type']} signal => {cryptos[key]}")