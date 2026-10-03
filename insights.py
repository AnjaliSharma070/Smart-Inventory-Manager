def create_summary(df):

    summary = {

        "total_products":
            int(
                df["Product_ID"]
                .nunique()
            ),

        "total_stock":
            int(
                df["Stock"]
                .sum()
            ),

        "total_sales":
            int(
                df["Units_Sold"]
                .sum()
            ),

        "total_revenue":
            float(
                df["Revenue"]
                .sum()
            ),

        "fast_moving":
            int(
                (
                    df["Movement_Status"]
                    == "Fast-Moving"
                ).sum()
            ),

        "normal_moving":
            int(
                (
                    df["Movement_Status"]
                    == "Normal-Moving"
                ).sum()
            ),

        "slow_moving":
            int(
                (
                    df["Movement_Status"]
                    == "Slow-Moving"
                ).sum()
            ),

        "anomalies":
            int(
                (
                    df["Anomaly"]
                    == "Anomaly"
                ).sum()
            )
    }

    return summary


def generate_insights(df):

    insights = []

    # Fast-moving product
    fast_products = df[
        df["Movement_Status"]
        == "Fast-Moving"
    ]

    if not fast_products.empty:

        product = fast_products.loc[
            fast_products["Units_Sold"].idxmax(),
            "Product_Name"
        ]

        insights.append(
            f"{product} is one of the highest "
            f"sales fast-moving products."
        )

    # Slow-moving product
    slow_products = df[
        df["Movement_Status"]
        == "Slow-Moving"
    ]

    if not slow_products.empty:

        product = slow_products.loc[
            slow_products["Units_Sold"].idxmin(),
            "Product_Name"
        ]

        insights.append(
            f"{product} has relatively "
            f"low sales movement."
        )

    # Anomaly
    anomalies = df[
        df["Anomaly"]
        == "Anomaly"
    ]

    if not anomalies.empty:

        product = anomalies.iloc[
            0
        ]["Product_Name"]

        insights.append(
            f"Unusual activity detected "
            f"for {product}. Review its "
            f"inventory activity."
        )

    # Highest-selling category
    category_sales = (
        df.groupby("Category")
        ["Units_Sold"]
        .sum()
    )

    if not category_sales.empty:

        category = (
            category_sales
            .idxmax()
        )

        insights.append(
            f"{category} has the highest "
            f"total unit sales."
        )

    return insights