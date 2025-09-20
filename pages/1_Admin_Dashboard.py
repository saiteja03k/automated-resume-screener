import streamlit as st
import pandas as pd
from utils.db_utils import get_all_evaluations

# --- Page Configuration ---
st.set_page_config(
    page_title="Admin Dashboard",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Placement Team Dashboard")
st.markdown("Review, filter, and analyze all student resume evaluations.")

# --- Simple Password Protection ---
def check_password():
    """Returns `True` if the user had the correct password."""
    password = st.sidebar.text_input("Enter Admin Password", type="password")
    if password == "admin123":
        return True
    elif password:
        st.sidebar.warning("Password incorrect. Please try again.")
        return False
    else:
        return False

if check_password():
    st.sidebar.header("Filters")
    all_results_df = get_all_evaluations()

    if not all_results_df.empty:
        # --- NEW: Job Title Filter ---
        job_filter = st.sidebar.text_input("Filter by Job Title:")

        # --- Verdict Filter ---
        verdict_filter = st.sidebar.multiselect(
            'Filter by Verdict:',
            options=all_results_df['verdict'].unique(),
            default=all_results_df['verdict'].unique()
        )
        
        # --- Score Filter ---
        score_filter = st.sidebar.slider(
            'Filter by Relevance Score:',
            min_value=0, max_value=100, 
            value=(0, 100)
        )
        
        # --- Apply filters ---
        # Start with the full dataframe
        filtered_df = all_results_df

        # Apply each filter sequentially
        if job_filter:
            filtered_df = filtered_df[filtered_df['job_title'].str.contains(job_filter, case=False, na=False)]
        
        filtered_df = filtered_df[
            (filtered_df['verdict'].isin(verdict_filter)) &
            (filtered_df['relevance_score'].between(score_filter[0], score_filter[1]))
        ]

        # --- Display the Dashboard ---
        st.header("All Evaluation Results")
        st.markdown("Click on a column header to sort the data.")
        
        # Improve display format
        filtered_df['evaluation_date'] = pd.to_datetime(filtered_df['evaluation_date']).dt.strftime('%Y-%m-%d %H:%M')
        filtered_df = filtered_df.sort_values(by="relevance_score", ascending=False)
        
        st.dataframe(filtered_df, use_container_width=True)
    else:
        st.info("No evaluations have been run yet from the student submission portal.")
else:
    st.info("Please enter the password in the sidebar to view the dashboard.")