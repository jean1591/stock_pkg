# FILES
from utils import update_db, generate_log, display_results, divide_crypto, undivide_crypto, calculate_metrics
from stock import OHLCV, Interval, Window, Indicators
from strategy import apply_strategy, p_ma_squeeze, p_ma_squeeze_short


# PACKAGES
import math
from pprint import pprint
import csv
from datetime import datetime
import pandas as pd
from pprint import pprint
import matplotlib.pyplot as plt


cryptos = ["BTC-USD", "ETH-USD", "MIOTA-USD"]
# cryptos = ["MIOTA-USD"]
df_list = []

# For each ticker in cryptos => Fetch stock data, apply strategy and append to df_list
for crypto in cryptos:
  c_df = OHLCV.fetch(crypto, window=Window.TWO_YEARS, indicators=[Indicators.MA])
  df_list.append(apply_strategy(c_df, p_ma_squeeze))

wallet = 5000
portfolio = {k:{"qty": 0} for k in cryptos}
ledger = []

print(f"BACKTEST: {datetime.now().strftime('%Y-%m-%d (%H:%M)')}")
print(f">> Start Date: {df_list[0].index[0].strftime('%Y-%m-%d (%H:%M)')}")
print(f">> End Date: {df_list[0].index[-1].strftime('%Y-%m-%d (%H:%M)')}")


# Loop dates
for d in df_list[0].index:
  # Loop df
  for key, df in enumerate(df_list):
    try:
      # Current Date DataFrame => c_d_df
      c_d_df = df.loc[d].to_dict()

      # Orders
      if c_d_df["order_type"] == "buy" or c_d_df["order_type"] == "sell":
        # Current close
        close = c_d_df["close"]

        # BTC & ETH can be splitted
        close = divide_crypto(cryptos[key], ["BTC-USD", "ETH-USD"], close, 100)
        
        # Update wallet, ledger & portfolio
        wallet, ledger, portfolio = update_db(wallet, ledger, portfolio, d, cryptos[key], c_d_df["order_type"], close)

    except KeyError as e:
      print(f"KeyError -- {cryptos[key]} -- {e}")


# ROI
portfolio = undivide_crypto(["BTC-USD", "ETH-USD"], portfolio, 100)
portfolio_value, overall_value, roi = calculate_metrics(portfolio, df_list, cryptos, wallet, 5000)

display_results(cryptos, 5000, wallet, portfolio, portfolio_value, overall_value, roi)
generate_log(ledger)


ledger_df = pd.DataFrame(ledger)
ledger_df.columns = ["date", "symbol", "order_type", "close", "qty", "order_value"]

signals_df = {}
for crypto in cryptos:
  signals_df[crypto] = {}
  buy_df = ledger_df[(ledger_df["symbol"] == crypto) & (ledger_df["order_type"] == "buy")].copy()
  sell_df = ledger_df[(ledger_df["symbol"] == crypto) & (ledger_df["order_type"] == "sell")].copy()

  # Set date col to type date
  buy_df["date"] = pd.to_datetime(buy_df["date"])
  sell_df["date"] = pd.to_datetime(sell_df["date"])

  # Set index
  buy_df.set_index("date", inplace=True)
  sell_df.set_index("date", inplace=True)

  signals_df[crypto]["buy"] = buy_df
  signals_df[crypto]["sell"] = sell_df





fig, (main_plot, sec_plot, third_plot) = plt.subplots(3, 1, sharex=True, figsize=(20, 10), gridspec_kw={"height_ratios": [1, 1, 1]})

ma_1, ma_2 = "ma_20", "ma_50"

for key, c_plot in enumerate([main_plot, sec_plot, third_plot]):
  # Plot Close
  c_plot.plot(df_list[key].index, df_list[key]["close"], label=f"{cryptos[key]} (close)")

  # Plot MA
  c_plot.plot(df_list[key].index, df_list[key][ma_1], label=ma_1, color="green", alpha=0.2)
  c_plot.plot(df_list[key].index, df_list[key][ma_2], label=ma_2, color="red", alpha=0.2)

  # Fill MA
  c_plot.fill_between(df_list[key].index, df_list[key][ma_1], df_list[key][ma_2], where=df_list[key][ma_1] > df_list[key][ma_2], facecolor="green", interpolate=True, alpha=0.1)
  c_plot.fill_between(df_list[key].index, df_list[key][ma_2], df_list[key][ma_1], where=df_list[key][ma_2] > df_list[key][ma_1], facecolor="red", interpolate=True, alpha=0.1)

  # Tools
  c_plot.legend()
  c_plot.grid()
  
  # Markers
  ## Get current stock signals
  c_buy = signals_df[cryptos[key]]["buy"]
  c_sell = signals_df[cryptos[key]]["sell"]

  ## Plot signals
  c_plot.plot(c_buy.index, c_buy["close"] if cryptos[key] == "MIOTA-USD" else c_buy["close"] * 100, "^", ms=5, color="green")
  c_plot.plot(c_sell.index, c_sell["close"] if cryptos[key] == "MIOTA-USD" else c_sell["close"] * 100, "v", ms=5, color="red")

# Figure
fig.suptitle(f"{', '.join(cryptos)}")
fig.tight_layout()

# Plot
plt.show()