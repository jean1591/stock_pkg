# PACKAGES
from datetime import datetime
import csv


def generate_log(lst):
  try:
    cols = ["date", "symbol", "order_type", "close", "qty", "order_value"]
    lst.insert(0, cols)
    with open("activity.csv", "w+") as my_csv:
      csvWriter = csv.writer(my_csv,delimiter=',')
      csvWriter.writerows(lst)
      print("Logs generated")
  except Exception as e:
    print(f"Exception -- {e}")

