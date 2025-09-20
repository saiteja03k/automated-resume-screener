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
    if password == "admin123": # You can change this simple password
        return True
    elif password: # If a password was entered but is incorrect
        st.sidebar.warning("Password incorrect. Please try again.")
        return False
    else:
        return False

if check_password():
    # --- Dashboard View ---
    st.header("All Evaluation Results")
    st.markdown("Click on a column header to sort the data.")

    all_results_df = get_all_evaluations()

    if not all_results_df.empty:
        # Improve display
        all_results_df['evaluation_date'] = pd.to_datetime(all_results_df['evaluation_date']).dt.strftime('%Y-%m-%d %H:%M')
        all_results_df = all_results_df.sort_values(by="relevance_score", ascending=False)
        
        # Add filters
        st.sidebar.header("Filters")
        verdict_filter = st.sidebar.multiselect(
            'Filter by Verdict:',
            options=all_results_df['verdict'].unique(),
            default=all_results_df['verdict'].unique()
        )
        
        score_filter = st.sidebar.slider(
            'Filter by Relevance Score:',
            min_value=0, max_value=100, 
            value=(0, 100)
        )
        
        # Apply filters
        filtered_df = all_results_df[
            (all_results_df['verdict'].isin(verdict_filter)) &
            (all_results_df['relevance_score'].between(score_filter[0], score_filter[1]))
        ]

        st.dataframe(filtered_df, use_container_width=True)
    else:
        st.info("No evaluations have been run yet from the student submission portal.")
else:
    st.info("Please enter the password in the sidebar to view the dashboard.")