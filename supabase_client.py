import streamlit as st
from supabase import create_client


@st.cache_resource
def get_supabase_client():
    supabase_url = st.secrets["SUPABASE_URL"]

    supabase_key = (
        st.secrets.get("SUPABASE_PUBLISHABLE_KEY")
        or st.secrets.get("SUPABASE_ANON_KEY")
    )

    if not supabase_url or not supabase_key:
        raise ValueError("Supabase URL or publishable key is missing.")

    return create_client(supabase_url, supabase_key)
