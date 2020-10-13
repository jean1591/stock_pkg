# FILES
from utils import get_stock, update_db, generate_log, display_results, divide_crypto, undivide_crypto, calculate_metrics
from stock import Indicators


# PACKAGES
import math
from pprint import pprint
import csv
from datetime import datetime


cryptos = ["BTC-USD", "ETH-USD", "MIOTA-USD"]
# cryptos = ["MIOTA-USD"]
df_list = []
for crypto in cryptos:
  df_list.append(get_stock(crypto, indicators=[Indicators.MA]))

wallet = 5000
portfolio = {k:{"qty": 0} for k in cryptos}
ledger = []


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
      print(f"KeyError -- {e}")


# ROI
portfolio = undivide_crypto(["BTC-USD", "ETH-USD"], portfolio, 100)
portfolio_value, overall_value, roi = calculate_metrics(portfolio, df_list, cryptos, wallet, 5000)

display_results(cryptos, 5000, wallet, portfolio, portfolio_value, overall_value, roi)
generate_log(ledger)