# FILES
from stock import OHLCV, Interval, Window, Indicators

# PACKAGES
import math


def check_wallet(wallet, close, qty):
  """
  Check if wallet can buy stocks

  Args:
      wallet (int): Wallet to check
      close (float): Current closing price
      qty (int): Quantity to buy

  Returns:
      bool: True if order can be passed, False otherwise
  """
  return wallet / 3 >= close * qty


def check_portfolio(portfolio, symbol):
  """
  Check if portfolio can sell stocks

  Args:
      portfolio (object): Stock portfolio
      symbol (string): Stock to check

  Returns:
      bool: True if order can be passed, False otherwise
  """
  try:
    return portfolio[symbol]["qty"] >= 3
  except KeyError as e:
    print(f"KeyError -- {e}")
    return 0


def calculate_qty(wallet, portfolio, symbol, order_type, close):
  """
  Calculate quantity to buy or sell given a wallet / portfolio

  Args:
      wallet (int): Wallet with which to buy
      portfolio (object): Stock portfolio
      symbol (string): Stock to check
      order_type (string): Either "buy" or "sell"
      close (float): Current closing price

  Returns:
      int: A quantity to buy or sell
  """
  if order_type == "buy":
    return math.floor(math.floor(wallet / 3) / close)
  elif order_type == "sell":
    return math.floor(portfolio[symbol]["qty"] / 3)


def divide_crypto(crypto, cryptos, close, divisor):
  if crypto in cryptos:
    close = close / divisor
  return close

def undivide_crypto(cryptos, portfolio, divisor):
  for crypto in cryptos:
    if crypto in portfolio.keys():
      portfolio[crypto]["qty"] = portfolio[crypto]["qty"] / divisor
  return portfolio


def display_results(cryptos, initial_wallet, wallet, portfolio, portfolio_value, overall_value, roi):
  print(f"Starting analysis on {', '.join(cryptos)}:")
  print(f"Wallet start: €{round(initial_wallet, 2)}")
  print(f"Wallet end: €{round(wallet, 2)}")
  print(f"Portfolio: {portfolio}")
  print(f"Portfolio value: €{round(portfolio_value, 2)}")
  print(f"Wallet + Portfolio value: €{round(overall_value, 2)}")
  print(f"ROI: {round(roi, 2)}%")
  print(f"Gain/Loss: €{round(overall_value - initial_wallet, 2)}")