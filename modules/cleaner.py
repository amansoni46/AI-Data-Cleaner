import pandas as pd


def clean_data(df):
    cleaned_df = df.copy()

    # Remove completely empty rows
    cleaned_df = cleaned_df.dropna(how="all")

    # Remove completely empty columns
    cleaned_df = cleaned_df.dropna(axis=1, how="all")

    # Remove duplicate rows
    cleaned_df = cleaned_df.drop_duplicates()

    # Clean column names
    cleaned_df.columns = cleaned_df.columns.str.strip()

    # Clean spaces from text values
    for column in cleaned_df.select_dtypes(include="object").columns:
        cleaned_df[column] = cleaned_df[column].str.strip()

    return cleaned_df