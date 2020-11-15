import numpy as np


def apply_strategy(df, strategy):
    return strategy(df)


def p_ma_squeeze(stock_df):
    # Delete useless cols
    cols = ["close", "ma_20", "ma_50"]
    stock_df = stock_df.loc[:, cols]

    # Add p_ma cols
    stock_df["p_ma"] = (100 - (stock_df["ma_50"] / stock_df["ma_20"] * 100)).round(decimals=2)

    buy = (
        (stock_df["close"] < stock_df["ma_20"] * 1.05) &
        (stock_df["p_ma"] < -10) &
        (stock_df["p_ma"].shift() < stock_df["p_ma"]) &
        (stock_df["p_ma"].shift() <= stock_df["p_ma"].shift(2))
    )

    sell = (
        (stock_df["close"] > stock_df["ma_20"] * 0.95) &
        (stock_df["p_ma"] > 10) &
        (stock_df["p_ma"].shift() > stock_df["p_ma"]) &
        (stock_df["p_ma"].shift() >= stock_df["p_ma"].shift(2))
    )

    # Conditions
    condition_list = [buy, sell]

    # Condition results
    choice_list = ["buy", "sell"]

    # Apply
    stock_df["order_type"] = np.select(condition_list, choice_list, default=None)

    return stock_df


def p_ma_squeeze_short(stock_df):
    # Delete useless cols
    cols = ["close", "ma_100", "ma_200"]
    stock_df = stock_df.loc[:, cols]

    # Add p_ma cols
    stock_df["p_ma"] = (100 - (stock_df["ma_200"] / stock_df["ma_100"] * 100)).round(decimals=2)

    buy = (
        (stock_df["close"] < stock_df["ma_100"] * 1.05) &
        (stock_df["p_ma"] < -10) &
        (stock_df["p_ma"].shift() < stock_df["p_ma"]) &
        (stock_df["p_ma"].shift() <= stock_df["p_ma"].shift(2))
    )

    sell = (
        (stock_df["close"] > stock_df["ma_100"] * 0.95) &
        (stock_df["p_ma"] > 10) &
        (stock_df["p_ma"].shift() > stock_df["p_ma"]) &
        (stock_df["p_ma"].shift() >= stock_df["p_ma"].shift(2))
    )

    # Conditions
    condition_list = [buy, sell]

    # Condition results
    choice_list = ["buy", "sell"]

    # Apply
    stock_df["order_type"] = np.select(condition_list, choice_list, default=None)

    return stock_df