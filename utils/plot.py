# PACKAGES
import matplotlib.pyplot as plt
import math
import numpy as np
import pandas as pd



def plot_two(stock_df, buy_df, sell_df, name):
    # Create fig
    fig, (main_plot, sec_plot) = plt.subplots(2, 1, sharex=True, figsize=(30,15), gridspec_kw={"height_ratios": [3, 1]})

    # Main plot
    # Plot main line
    main_plot.plot(stock_df.index, stock_df["close"], label="close")

    # Plot secondary lines
    main_plot.plot(stock_df.index, stock_df["ma_20"], alpha=0.5, label="ma_20")
    main_plot.plot(stock_df.index, stock_df["ma_50"], alpha=0.5, label="ma_50")
    # main_plot.scatter(stock_df.index, stock_df["psar"], color="red", label="psar", s=1)

    # Plot areas / lines
    main_plot.fill_between(stock_df.index, stock_df["ma_20"], stock_df["ma_50"], where=stock_df["ma_20"] > stock_df["ma_50"], facecolor="green", interpolate=True, alpha=0.05)
    main_plot.fill_between(stock_df.index, stock_df["ma_20"], stock_df["ma_50"], where=stock_df["ma_20"] < stock_df["ma_50"], facecolor="red", interpolate=True, alpha=0.05)

    # Plot markers
    # Sell
    main_plot.plot(sell_df["order_type"].index, sell_df["close"], "v", ms=10, color="red")
    # Buy
    main_plot.plot(buy_df["order_type"].index, buy_df["close"], "^", ms=10, color="green")

    # Tools
    main_plot.set_title("Close in regards of 20MA & 50MA")
    main_plot.grid()

    # yticks
    mini = math.floor(stock_df["close"].min())
    maxi = math.ceil(stock_df["close"].max())
    step = math.floor((maxi - mini) / 20) if math.floor((maxi - mini) / 20) != 0 else ((maxi - mini) / 20)
    main_plot.set_yticks(np.arange(mini, maxi, step), minor=False)  

    main_plot.legend(fontsize="x-large")

    # Secondary plot
    sec_plot.plot(stock_df.index, stock_df["p_band_ma_5"], color="orange", label="p_band_ma_5")
    sec_plot.bar(stock_df.index, stock_df["p_ma"], color="green", alpha=0.2, label="p_ma")

    # Plot areas / lines
    sec_plot.axhline(y=0, color="black")
    sec_plot.axhline(y=10, color="blue", alpha=0.2)

    # Plot markers
    # Sell
    sec_plot.plot(sell_df["order_type"].index, sell_df["p_band_ma_5"], "v", ms=10, color="red")
    # Buy
    sec_plot.plot(buy_df["order_type"].index, buy_df["p_band_ma_5"], "^", ms=10, color="green")

    # Tools
    sec_plot.set_title("Bollinger Band Squeeze v. MA Squeeze")
    sec_plot.grid()
    sec_plot.set_ylim([-10, 20])
    sec_plot.legend(fontsize="x-large")


    # Figure Spec
    fig.suptitle(f"{name.upper()}", fontsize=16)
    fig.tight_layout()

    # Save
    # fig.savefig(f"{c_symbol}.png", dpi=100, bbox_inches="tight")