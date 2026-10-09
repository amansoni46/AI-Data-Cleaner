import io
import json

import pandas as pd
import streamlit as st
import streamlit.components.v1 as components
from supabase import create_client

from modules.analyzer import analyze_data
from modules.cleaner import clean_data
from modules.report import generate_report
from supabase_client import get_supabase_client


# ----------------------------------------
# Page Configuration
# ----------------------------------------

st.set_page_config(
    page_title="AI Data Cleaner",
    page_icon="🧹",
    layout="wide",
)




# ----------------------------------------
# Authentication (Supabase)
# ----------------------------------------

def get_auth_client():
    """Create one auth client per Streamlit session, not a shared global client."""
    if "auth_client" not in st.session_state:
        supabase_url = st.secrets.get("SUPABASE_URL")
        publishable_key = (
            st.secrets.get("SUPABASE_PUBLISHABLE_KEY")
            or st.secrets.get("SUPABASE_ANON_KEY")
        )

        if not supabase_url or not publishable_key:
            st.error(
                "Authentication setup is incomplete. Add SUPABASE_URL and "
                "SUPABASE_PUBLISHABLE_KEY (or SUPABASE_ANON_KEY) to Streamlit Secrets."
            )
            st.stop()

        st.session_state["auth_client"] = create_client(
            supabase_url,
            publishable_key,
        )

    return st.session_state["auth_client"]


def save_auth_user(auth_response):
    user = getattr(auth_response, "user", None)
    if user is None:
        data = getattr(auth_response, "data", None)
        user = getattr(data, "user", None) if data else None

    if user is not None:
        st.session_state["auth_user"] = {
            "id": getattr(user, "id", ""),
            "email": getattr(user, "email", ""),
        }


auth_client = get_auth_client()

# Handle the redirect back from Supabase after Google OAuth.
oauth_code = st.query_params.get("code")
if oauth_code and not st.session_state.get("auth_user"):
    try:
        oauth_response = auth_client.auth.exchange_code_for_session(oauth_code)
        save_auth_user(oauth_response)
        st.query_params.clear()
        if st.session_state.get("auth_user"):
            st.rerun()
        else:
            st.error("Google login completed, but no user session was returned.")
    except Exception as exc:
        st.error("Google sign-in could not be completed. Please try again.")
        st.caption(f"Technical details: {exc}")
        st.query_params.clear()

# Show the login screen until the user is authenticated.
if not st.session_state.get("auth_user"):
    st.title("🧹 AI Data Cleaner")
    st.subheader("Sign in to continue")
    st.write("Log in with your email and password, create an account, or use Google.")

    login_tab, signup_tab = st.tabs(["Login", "Create account"])

    with login_tab:
        with st.form("login_form"):
            login_email = st.text_input("Email address", key="login_email")
            login_password = st.text_input(
                "Password", type="password", key="login_password"
            )
            login_submitted = st.form_submit_button(
                "Login", type="primary", use_container_width=True
            )

        if login_submitted:
            if not login_email.strip() or not login_password:
                st.warning("Please enter both your email and password.")
            else:
                try:
                    result = auth_client.auth.sign_in_with_password(
                        {
                            "email": login_email.strip(),
                            "password": login_password,
                        }
                    )
                    save_auth_user(result)
                    if st.session_state.get("auth_user"):
                        st.success("Login successful!")
                        st.rerun()
                    else:
                        st.error("Login did not return a user session.")
                except Exception:
                    st.error(
                        "Login failed. Check your email and password, "
                        "or create an account first."
                    )

    with signup_tab:
        with st.form("signup_form"):
            signup_email = st.text_input("Email address", key="signup_email")
            signup_password = st.text_input(
                "Create password (minimum 6 characters)",
                type="password",
                key="signup_password",
            )
            signup_confirm = st.text_input(
                "Confirm password", type="password", key="signup_confirm"
            )
            signup_submitted = st.form_submit_button(
                "Create account", type="primary", use_container_width=True
            )

        if signup_submitted:
            if not signup_email.strip() or not signup_password:
                st.warning("Please enter an email and password.")
            elif len(signup_password) < 6:
                st.warning("Use a password with at least 6 characters.")
            elif signup_password != signup_confirm:
                st.warning("The passwords do not match.")
            else:
                try:
                    result = auth_client.auth.sign_up(
                        {
                            "email": signup_email.strip(),
                            "password": signup_password,
                        }
                    )
                    if getattr(result, "session", None):
                        save_auth_user(result)
                        st.success("Account created successfully!")
                        st.rerun()
                    else:
                        st.success(
                            "Account created. Check your email for the confirmation "
                            "link, then return here and log in."
                        )
                except Exception:
                    st.error(
                        "Account creation failed. The email may already be registered "
                        "or Supabase may have rejected the signup."
                    )

    st.divider()
    st.markdown("#### Or continue with Google")

    if st.button("Continue with Google", use_container_width=True):
        try:
            app_url = st.secrets.get(
                "APP_URL", "http://localhost:8501"
            ).rstrip("/")
            result = auth_client.auth.sign_in_with_oauth(
                {
                    "provider": "google",
                    "options": {"redirect_to": app_url},
                }
            )
            oauth_url = getattr(result, "url", None)
            if not oauth_url:
                data = getattr(result, "data", None)
                oauth_url = getattr(data, "url", None) if data else None

            if oauth_url:
                # Navigate in the same browser tab to preserve the OAuth flow.
                components.html(
                    f"""
                    <script>
                    window.top.location.href = {json.dumps(oauth_url)};
                    </script>
                    """,
                    height=0,
                )
                st.info("Opening Google sign-in…")
            else:
                st.error("Supabase did not return a Google sign-in URL.")
        except Exception as exc:
            st.error("Unable to start Google sign-in.")
            st.caption(f"Technical details: {exc}")

    st.stop()


# ----------------------------------------
# Header
# ----------------------------------------

st.title("🧹 AI Data Cleaner")

st.write(
    "Upload your CSV or Excel file to analyze data quality, "
    "clean your dataset, and download the cleaned file."
)

st.caption("Smart Data Cleaning • Quality Analysis • Cleaning History")


# ----------------------------------------
# Sidebar
# ----------------------------------------

with st.sidebar:
    st.header("🧹 AI Data Cleaner")
    st.write("Clean your data and review previous cleaning records.")
    current_user = st.session_state.get("auth_user", {})
    st.caption(f"Signed in: {current_user.get('email', 'user')}")
    if st.button("Log out", use_container_width=True):
        try:
            auth_client.auth.sign_out()
        except Exception:
            pass
        st.session_state.pop("auth_user", None)
        st.session_state.pop("cleaned_df", None)
        st.session_state.pop("cleaning_report", None)
        st.session_state.pop("cleaned_file_name", None)
        st.rerun()
    st.divider()

    page = st.radio(
        "Navigation",
        ["Data Cleaner", "Cleaning History"],
    )


# ----------------------------------------
# Cleaning History Page
# ----------------------------------------

if page == "Cleaning History":

    st.header("📋 Cleaning History")

    st.write(
        "View previous cleaning operations saved in Supabase."
    )

    if st.button("🔄 Refresh History") or True:
        try:
            supabase = get_supabase_client()

            response = (
                supabase
                .table("cleaning_history")
                .select(
                    "id, file_name, original_rows, cleaned_rows, "
                    "rows_removed, columns_removed, created_at"
                )
                .order("created_at", desc=True)
                .limit(100)
                .execute()
            )

            history = response.data or []

            if history:
                history_df = pd.DataFrame(history)

                st.success(
                    f"Loaded {len(history_df)} cleaning record(s)."
                )

                st.dataframe(
                    history_df,
                    use_container_width=True,
                    hide_index=True,
                )

                csv_history = history_df.to_csv(
                    index=False
                ).encode("utf-8")

                st.download_button(
                    "⬇️ Download Cleaning History",
                    data=csv_history,
                    file_name="cleaning_history.csv",
                    mime="text/csv",
                )

            else:
                st.info(
                    "No cleaning history found yet. "
                    "Clean a dataset to create your first record."
                )

        except Exception as e:
            st.error(
                "Unable to load cleaning history. "
                "Check your Supabase configuration and database permissions."
            )
            st.caption(f"Technical details: {e}")


# ----------------------------------------
# Data Cleaner Page
# ----------------------------------------

else:

    st.header("📁 Upload Dataset")

    uploaded_file = st.file_uploader(
        "Choose a CSV or Excel file",
        type=["csv", "xlsx"],
    )

    if uploaded_file is not None:

        try:
            # Read the uploaded file
            if uploaded_file.name.lower().endswith(".csv"):
                df = pd.read_csv(uploaded_file)
            else:
                df = pd.read_excel(uploaded_file)

            if df.empty:
                st.warning(
                    "The uploaded file contains no data rows."
                )

            st.success("File uploaded successfully! ✅")

            # ----------------------------------------
            # Dataset Preview
            # ----------------------------------------

            st.subheader("📊 Original Dataset Preview")

            st.dataframe(
                df.head(20),
                use_container_width=True,
            )

            # ----------------------------------------
            # Data Quality Analysis
            # ----------------------------------------

            analysis = analyze_data(df)

            st.subheader("🔍 Data Quality Analysis")

            col1, col2, col3, col4 = st.columns(4)

            with col1:
                st.metric(
                    "Total Rows",
                    analysis["rows"],
                )

            with col2:
                st.metric(
                    "Total Columns",
                    analysis["columns"],
                )

            with col3:
                st.metric(
                    "Duplicate Rows",
                    analysis["duplicate_rows"],
                )

            with col4:
                st.metric(
                    "Columns with Empty Data",
                    len(analysis["empty_columns"]),
                )

            # ----------------------------------------
            # Missing Values
            # ----------------------------------------

            st.subheader("⚠️ Missing Values")

            if analysis["missing_values"]:

                missing_df = pd.DataFrame(
                    list(analysis["missing_values"].items()),
                    columns=["Column", "Missing Values"],
                )

                st.dataframe(
                    missing_df,
                    use_container_width=True,
                    hide_index=True,
                )

            else:
                st.success("No missing values found! ✅")

            # ----------------------------------------
            # Data Types
            # ----------------------------------------

            st.subheader("🔤 Data Types")

            datatype_df = pd.DataFrame(
                list(analysis["data_types"].items()),
                columns=["Column", "Data Type"],
            )

            st.dataframe(
                datatype_df,
                use_container_width=True,
                hide_index=True,
            )

            # ----------------------------------------
            # Clean Dataset
            # ----------------------------------------

            st.subheader("🧹 Clean Dataset")

            if st.button(
                "✨ Clean Data",
                type="primary",
                use_container_width=True,
            ):

                cleaned_df = clean_data(df)

                report = generate_report(
                    df,
                    cleaned_df,
                )

                st.session_state["cleaned_df"] = cleaned_df
                st.session_state["cleaning_report"] = report
                st.session_state["cleaned_file_name"] = (
                    uploaded_file.name
                )

                # ----------------------------------------
                # Save History to Supabase
                # ----------------------------------------

                try:
                    supabase = get_supabase_client()

                    history_data = {
                        "file_name": uploaded_file.name,
                        "original_rows": int(
                            report["original_rows"]
                        ),
                        "cleaned_rows": int(
                            report["cleaned_rows"]
                        ),
                        "rows_removed": int(
                            report["rows_removed"]
                        ),
                        "columns_removed": int(
                            report["columns_removed"]
                        ),
                    }

                    (
                        supabase
                        .table("cleaning_history")
                        .insert(history_data)
                        .execute()
                    )

                    st.session_state[
                        "history_save_message"
                    ] = (
                        "Cleaning history saved to Supabase! ✅"
                    )

                except Exception as e:
                    st.session_state[
                        "history_save_message"
                    ] = (
                        "The data was cleaned, but its history "
                        "could not be saved to Supabase."
                    )

                    st.session_state[
                        "history_save_error"
                    ] = str(e)

            # ----------------------------------------
            # Display Cleaning Results
            # ----------------------------------------

            if "cleaned_df" in st.session_state:

                cleaned_df = st.session_state["cleaned_df"]
                report = st.session_state["cleaning_report"]

                st.divider()

                st.success("Data cleaned successfully! ✅")

                if st.session_state.get("history_save_message"):
                    st.info(
                        st.session_state["history_save_message"]
                    )

                if st.session_state.get("history_save_error"):
                    with st.expander(
                        "Why wasn't the history saved?"
                    ):
                        st.code(
                            st.session_state["history_save_error"]
                        )

                # Cleaning Report
                st.subheader("📋 Cleaning Report")

                r1, r2, r3, r4 = st.columns(4)

                with r1:
                    st.metric(
                        "Original Rows",
                        report["original_rows"],
                    )

                with r2:
                    st.metric(
                        "Cleaned Rows",
                        report["cleaned_rows"],
                    )

                with r3:
                    st.metric(
                        "Rows Removed",
                        report["rows_removed"],
                    )

                with r4:
                    st.metric(
                        "Columns Removed",
                        report["columns_removed"],
                    )

                # Cleaned Data Preview
                st.subheader("✨ Cleaned Dataset")

                st.dataframe(
                    cleaned_df.head(20),
                    use_container_width=True,
                )

                # ----------------------------------------
                # Download CSV
                # ----------------------------------------

                csv_data = cleaned_df.to_csv(
                    index=False
                ).encode("utf-8")

                st.download_button(
                    label="⬇️ Download Clean CSV",
                    data=csv_data,
                    file_name="cleaned_data.csv",
                    mime="text/csv",
                    use_container_width=True,
                )

                # ----------------------------------------
                # Download Excel
                # ----------------------------------------

                excel_buffer = io.BytesIO()

                with pd.ExcelWriter(
                    excel_buffer,
                    engine="openpyxl",
                ) as writer:

                    cleaned_df.to_excel(
                        writer,
                        index=False,
                        sheet_name="Cleaned Data",
                    )

                st.download_button(
                    label="⬇️ Download Clean Excel",
                    data=excel_buffer.getvalue(),
                    file_name="cleaned_data.xlsx",
                    mime=(
                        "application/vnd.openxmlformats-officedocument."
                        "spreadsheetml.sheet"
                    ),
                    use_container_width=True,
                )

        except Exception as e:
            st.error(
                f"Something went wrong: {e}"
            )

    else:
        st.info(
            "👆 Upload a CSV or Excel file to get started."
        )
