import pandas as pd
import numpy as np

REQUIRED_COLUMNS = [
    "Product_ID",
    "Product_Name",
    "Category",
    "Stock",
    "Units_Sold",
    "Price",
    "Date",
    "Supplier"
]


def load_data(source):
    """
    Load CSV or Excel inventory dataset.
    """

    if hasattr(source, "name"):
        file_name = source.name.lower()
    else:
        file_name = str(source).lower()

    if file_name.endswith((".xlsx", ".xls")):
        df = pd.read_excel(source)

    elif file_name.endswith(".csv"):
        df = pd.read_csv(source)

    else:
        raise ValueError(
            "Unsupported file format. Please upload CSV or Excel file."
        )

    return df


def clean_data(df):
    """
    Clean and validate inventory data.
    """

    df = df.copy()

    # Clean column names
    df.columns = [
        str(column).strip()
        for column in df.columns
    ]

    # Check required inventory columns
    missing_columns = [
        column
        for column in REQUIRED_COLUMNS
        if column not in df.columns
    ]

    if missing_columns:

        raise ValueError(
            "The uploaded file is missing required inventory columns: "
            + ", ".join(missing_columns)
        )

    # Remove duplicate records
    df = df.drop_duplicates()

    # Numerical columns
    numerical_columns = [
        "Stock",
        "Units_Sold",
        "Price"
    ]

    for column in numerical_columns:

        df[column] = pd.to_numeric(
            df[column],
            errors="coerce"
        )

        median_value = df[column].median()

        if pd.isna(median_value):
            median_value = 0

        df[column] = df[column].fillna(
            median_value
        )

    # Prevent negative inventory values
    df["Stock"] = df["Stock"].clip(lower=0)

    df["Units_Sold"] = df["Units_Sold"].clip(lower=0)

    df["Price"] = df["Price"].clip(lower=0)

    # Date conversion
    df["Date"] = pd.to_datetime(
        df["Date"],
        errors="coerce"
    )

    if df["Date"].isna().all():

        df["Date"] = pd.Timestamp.today()

    else:

        df["Date"] = df["Date"].fillna(
            df["Date"].median()
        )

    # Text columns
    text_columns = [
        "Product_ID",
        "Product_Name",
        "Category",
        "Supplier"
    ]

    for column in text_columns:

        df[column] = (
            df[column]
            .fillna("Unknown")
            .astype(str)
            .str.strip()
        )

    return df.reset_index(drop=True)