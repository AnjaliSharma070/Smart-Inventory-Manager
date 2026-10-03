import numpy as np

from sklearn.ensemble import IsolationForest


ANOMALY_FEATURES = [
    "Stock",
    "Units_Sold",
    "Revenue",
    "Sales_Frequency",
    "Stock_Utilization",
    "Stock_Turnover"
]


def run_anomaly_detection(
    df,
    anomaly_rate=0.10
):

    df = df.copy()

    X = df[
        ANOMALY_FEATURES
    ].copy()

    # Replace infinity
    X = X.replace(
        [np.inf, -np.inf],
        np.nan
    )

    # Fill missing values
    X = X.fillna(0)

    # Limit anomaly rate
    anomaly_rate = min(
        max(
            float(anomaly_rate),
            0.01
        ),
        0.49
    )

    # Isolation Forest
    model = IsolationForest(
        contamination=anomaly_rate,
        random_state=42,
        n_estimators=200
    )

    predictions = model.fit_predict(X)

    scores = model.decision_function(X)

    # Label anomalies
    df["Anomaly"] = np.where(
        predictions == -1,
        "Anomaly",
        "Normal"
    )

    df["Anomaly_Score"] = scores

    return df, model