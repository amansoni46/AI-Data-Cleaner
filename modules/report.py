def generate_report(before, after):
    """
    Generate a basic cleaning report.
    """

    report = {
        "original_rows": len(before),
        "cleaned_rows": len(after),
        "rows_removed": len(before) - len(after),
        "original_columns": len(before.columns),
        "cleaned_columns": len(after.columns),
        "columns_removed": len(before.columns) - len(after.columns),
    }

    return report