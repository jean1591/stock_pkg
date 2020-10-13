# FILES
from utils import check_wallet, check_portfolio, calculate_qty


def update_wallet(wallet, order_type, close, qty):
  if order_type == "buy":
    wallet -= close * qty
  elif order_type == "sell":
    wallet += close * qty
  return wallet


def update_portfolio(portfolio, order_type, symbol, qty, close):
  if order_type == "buy":
    portfolio[symbol]["qty"] += qty
  elif order_type == "sell":
    portfolio[symbol]["qty"] -= qty
  return portfolio


def update_ledger(ledger, current_date, symbol, order_type, close, qty):
  ledger.append([current_date.strftime('%Y-%m-%d'), symbol, order_type, round(close, 2), qty, round(close * qty, 2)])
  return ledger


def update_db(wallet, ledger, portfolio, current_date, symbol, order_type, close):
  qty = calculate_qty(wallet, portfolio, symbol, order_type, close)
  
  # Order
  if (order_type == "buy" and check_wallet(wallet, close, qty) and qty > 0) or \
    (order_type == "sell" and check_portfolio(portfolio, symbol)):
    wallet = update_wallet(wallet, order_type, close, qty)
    portfolio = update_portfolio(portfolio, order_type, symbol, qty, close)
    ledger = update_ledger(ledger, current_date, symbol, order_type, close, qty)
  
  return wallet, ledger, portfolio


def calculate_portfolio_value(portfolio, df_list, cryptos):
  portfolio_value = 0
  for key, df in enumerate(df_list):
    portfolio_value += df.iloc[-1]["close"] * portfolio[cryptos[key]]["qty"]
  return portfolio_value


def calculate_overall_value(wallet, portfolio_value):
  return wallet + portfolio_value


def calculate_roi(overall_value, initial_wallet):
  return overall_value / initial_wallet * 100
  

def calculate_metrics(portfolio, df_list, cryptos, wallet, initial_wallet):
  portfolio_value = calculate_portfolio_value(portfolio, df_list, cryptos)
  overall_value = calculate_overall_value(wallet, portfolio_value)
  roi = calculate_roi(overall_value, initial_wallet)
  return [portfolio_value, overall_value, roi]

