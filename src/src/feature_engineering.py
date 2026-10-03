import numpy as np


def create_features(df):

    df = df.copy()

    # Revenue
    df["Revenue"] = (
        df["Units_Sold"] *
        df["Price"]
    )

    # Sales frequency
    df["Sales_Frequency"] = (
        df["Units_Sold"] /
        np.maximum(df["Stock"], 1)
    )

    # Stock utilization
    df["Stock_Utilization"] = (
        df["Units_Sold"] /
        np.maximum(
            df["Stock"] + df["Units_Sold"],
            1
        )
    )

    # Stock turnover
    df["Stock_Turnover"] = (
        df["Units_Sold"] /
        np.maximum(df["Stock"], 1)
    )

    # Avoid infinity values
    df = df.replace(
        [np.inf, -np.inf],
        0
    )

    return df