import streamlit as st
import pandas as pd

from modules.analyzer import analyze_data
from modules.cleaner import clean_data
from modules.report import generate_report


# -----------------------------
# Page Configuration
# -----------------------------

st.set_page_config(
    page_title="AI Data Cleaner",
    page_icon="🧹",
    layout="wide"
)


# -----------------------------
# Title
# -----------------------------

st.title("🧹 AI Data Cleaner")
st.write(
    "Upload your CSV or Excel file and analyze, clean and download your data."
)


# -----------------------------
# File Upload
# -----------------------------

uploaded_file = st.file_uploader(
    "Upload your data file",
    type=["csv", "xlsx"]
)


if uploaded_file is not None:

    # -----------------------------
    # Read File
    # -----------------------------

    try:

        if uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)

        else:
            df = pd.read_excel(uploaded_file)

        st.success("File uploaded successfully! ✅")

        # -----------------------------
        # Dataset Preview
        # -----------------------------

        st.subheader("📊 Data Preview")

        st.dataframe(
            df.head(20),
            use_container_width=True
        )

        # -----------------------------
        # Analyze Data
        # -----------------------------

        analysis = analyze_data(df)

        st.subheader("🔍 Data Quality Analysis")

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric(
                "Total Rows",
                analysis["rows"]
            )

        with col2:
            st.metric(
                "Total Columns",
                analysis["columns"]
            )

        with col3:
            st.metric(
                "Duplicate Rows",
                analysis["duplicate_rows"]
            )

        with col4:
            st.metric(
                "Columns with Empty Data",
                len(analysis["empty_columns"])
            )

        # -----------------------------
        # Missing Values
        # -----------------------------

        st.subheader("⚠️ Missing Values")

        if analysis["missing_values"]:

            missing_df = pd.DataFrame(
                list(
                    analysis["missing_values"].items()
                ),
                columns=["Column", "Missing Values"]
            )

            st.dataframe(
                missing_df,
                use_container_width=True
            )

        else:

            st.success("No missing values found! ✅")

        # -----------------------------
        # Data Types
        # -----------------------------

        st.subheader("🔤 Data Types")

        datatype_df = pd.DataFrame(
            list(
                analysis["data_types"].items()
            ),
            columns=["Column", "Data Type"]
        )

        st.dataframe(
            datatype_df,
            use_container_width=True
        )

        # -----------------------------
        # Clean Data Button
        # -----------------------------

        st.subheader("🧹 Clean Dataset")

        if st.button(
            "Clean Data",
            type="primary"
        ):

            cleaned_df = clean_data(df)

            report = generate_report(
                df,
                cleaned_df
            )

            st.success(
                "Data cleaned successfully! ✅"
            )

            # -----------------------------
            # Cleaning Report
            # -----------------------------

            st.subheader("📋 Cleaning Report")

            r1, r2, r3, r4 = st.columns(4)

            with r1:
                st.metric(
                    "Original Rows",
                    report["original_rows"]
                )

            with r2:
                st.metric(
                    "Cleaned Rows",
                    report["cleaned_rows"]
                )

            with r3:
                st.metric(
                    "Rows Removed",
                    report["rows_removed"]
                )

            with r4:
                st.metric(
                    "Columns Removed",
                    report["columns_removed"]
                )

            # -----------------------------
            # Cleaned Data Preview
            # -----------------------------

            st.subheader("✨ Cleaned Data")

            st.dataframe(
                cleaned_df.head(20),
                use_container_width=True
            )

            # -----------------------------
            # Download CSV
            # -----------------------------

            csv_data = cleaned_df.to_csv(
                index=False
            ).encode("utf-8")

            st.download_button(
                label="⬇️ Download Clean CSV",
                data=csv_data,
                file_name="cleaned_data.csv",
                mime="text/csv"
            )

            # -----------------------------
            # Download Excel
            # -----------------------------

            import io

            excel_buffer = io.BytesIO()

            with pd.ExcelWriter(
                excel_buffer,
                engine="openpyxl"
            ) as writer:

                cleaned_df.to_excel(
                    writer,
                    index=False,
                    sheet_name="Cleaned Data"
                )

            st.download_button(
                label="⬇️ Download Clean Excel",
                data=excel_buffer.getvalue(),
                file_name="cleaned_data.xlsx",
                mime=(
                    "application/"
                    "vnd.openxmlformats-officedocument."
                    "spreadsheetml.sheet"
                )
            )

    except Exception as e:

        st.error(
            f"Something went wrong: {e}"
        )