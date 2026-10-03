import numpy as np

from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler


ML_FEATURES = [
    "Stock",
    "Units_Sold",
    "Revenue",
    "Sales_Frequency",
    "Stock_Utilization",
    "Stock_Turnover"
]


def run_clustering(
    df,
    number_of_clusters=3
):

    df = df.copy()

    # Select ML features
    X = df[ML_FEATURES].copy()

    # Replace infinity
    X = X.replace(
        [np.inf, -np.inf],
        np.nan
    )

    # Fill missing values
    X = X.fillna(0)

    # Scaling
    scaler = StandardScaler()

    X_scaled = scaler.fit_transform(X)

    # Make sure clusters do not exceed rows
    number_of_clusters = min(
        max(2, number_of_clusters),
        len(df)
    )

    # K-Means
    model = KMeans(
        n_clusters=number_of_clusters,
        random_state=42,
        n_init=10
    )

    labels = model.fit_predict(
        X_scaled
    )

    df["Cluster"] = labels

    # Create cluster profile
    cluster_profile = (
        df.groupby("Cluster")
        [
            [
                "Units_Sold",
                "Revenue",
                "Stock_Turnover"
            ]
        ]
        .mean()
    )

    # Calculate cluster score
    cluster_score = (
        cluster_profile["Units_Sold"].rank(
            pct=True
        )
        +
        cluster_profile["Revenue"].rank(
            pct=True
        )
        +
        cluster_profile["Stock_Turnover"].rank(
            pct=True
        )
    )

    ordered_clusters = list(
        cluster_score
        .sort_values(
            ascending=False
        )
        .index
    )

    cluster_names = {}

    # Highest performing cluster
    if len(ordered_clusters) >= 1:

        cluster_names[
            ordered_clusters[0]
        ] = "Fast-Moving"

    # Lowest performing cluster
    if len(ordered_clusters) >= 2:

        cluster_names[
            ordered_clusters[-1]
        ] = "Slow-Moving"

    # Middle clusters
    for cluster in ordered_clusters[1:-1]:

        cluster_names[
            cluster
        ] = "Normal-Moving"

    df["Movement_Status"] = (
        df["Cluster"]
        .map(cluster_names)
        .fillna("Normal-Moving")
    )

    return (
        df,
        model,
        scaler
    )