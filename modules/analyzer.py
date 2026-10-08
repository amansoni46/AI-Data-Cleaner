import pandas as pd


def analyze_data(df):
    """
    Analyze uploaded dataset and return data-quality information.
    """

    analysis = {}

    # Basic dataset information
    analysis["rows"] = len(df)
    analysis["columns"] = len(df.columns)

    # Duplicate rows
    analysis["duplicate_rows"] = int(df.duplicated().sum())

    # Missing values
    missing_values = df.isnull().sum()
    analysis["missing_values"] = (
        missing_values[missing_values > 0].to_dict()
    )

    # Completely empty columns
    empty_columns = [
        column
        for column in df.columns
        if df[column].isnull().all()
    ]

    analysis["empty_columns"] = empty_columns

    # Data types
    analysis["data_types"] = {
        column: str(dtype)
        for column, dtype in df.dtypes.items()
    }

    return analysis