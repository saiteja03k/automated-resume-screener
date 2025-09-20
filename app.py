import streamlit as st
import pandas as pd
import os

# Import your custom modules
from core.parser import extract_text_from_file
from core.matcher import perform_hard_match
from core.scoring import get_embedding, perform_semantic_match, calculate_final_score, get_verdict, generate_feedback
from utils.db_utils import create_table, save_evaluation, get_all_evaluations

# --- Page Configuration ---
st.set_page_config(
    page_title="Automated Resume Relevance Checker",
    page_icon="📄",
    layout="wide"
)

# --- Main Application Logic ---

# Check for API Key
if "GEMINI_API_KEY" not in os.environ:
    st.error("🚨 Gemini API Key not found! Please set it as an environment variable.")
    st.stop()

# Initialize the database and table
create_table()

# --- UI Layout ---
st.title("🤖 Automated Resume Relevance Check System")
st.markdown("An AI-powered tool to score and rank resumes against job descriptions at scale. [cite: 1, 7]")

st.sidebar.header("Controls")

# --- Job Description Input ---
st.sidebar.subheader("1. Job Description")
jd_text = st.sidebar.text_area("Paste the Job Description here", height=200)

# --- Resume Files Upload ---
st.sidebar.subheader("2. Upload Resumes")
uploaded_files = st.sidebar.file_uploader(
    "Choose resume files (PDF or DOCX)", 
    type=['pdf', 'docx'], 
    accept_multiple_files=True
)

# --- Analysis Trigger ---
analyze_button = st.sidebar.button("Analyze Resumes", use_container_width=True)


# --- Results Display Area ---
st.header("Evaluation Results")

if analyze_button:
    if not jd_text:
        st.warning("Please paste a Job Description.")
    elif not uploaded_files:
        st.warning("Please upload at least one resume.")
    else:
        with st.spinner("Analyzing resumes... This may take a moment. 🧠"):
            # 1. Process Job Description
            jd_embedding = get_embedding(jd_text)
            
            if jd_embedding is None:
                st.error("Could not process the Job Description. The JD might be too short or there was an API error.")
                st.stop()

            # 2. Process Each Resume
            for resume_file in uploaded_files:
                st.markdown(f"---")
                st.subheader(f"Processing: `{resume_file.name}`")
                
                # Extract text
                resume_text = extract_text_from_file(resume_file)
                if "Error reading" in resume_text:
                    st.error(f"Could not read {resume_file.name}. Error: {resume_text}")
                    continue

                # Perform Hard Match
                hard_match_score, found, missing = perform_hard_match(jd_text, resume_text)
                
                # Perform Semantic Match
                resume_embedding = get_embedding(resume_text)
                semantic_score = perform_semantic_match(jd_embedding, resume_embedding)
                
                # Calculate Final Score and Verdict
                final_score = calculate_final_score(hard_match_score, semantic_score)
                verdict = get_verdict(final_score)
                
                # Generate AI Feedback
                feedback = generate_feedback(jd_text, resume_text, missing)

                # Save to Database
                job_title_placeholder = " ".join(jd_text.split()[:5]) + "..." # Use first few words as a title
                save_evaluation(job_title_placeholder, resume_file.name, final_score, verdict, missing, feedback)

                # Display Individual Result
                col1, col2, col3 = st.columns(3)
                col1.metric("Relevance Score", f"{final_score}%", delta=verdict)
                col2.metric("Keyword Match", f"{int(hard_match_score)}%")
                col3.metric("Semantic Match", f"{int(semantic_score)}%")

                with st.expander("Show Details & AI Feedback"):
                    st.markdown("##### AI-Generated Feedback for Improvement")
                    st.info(feedback)
                    st.markdown("##### Missing Keywords")
                    st.warning(", ".join(missing) if missing else "None")


# --- Dashboard View ---
st.markdown("---")
st.header("Results Dashboard")
st.markdown("All past evaluations are stored here. Click on a column to sort.")

all_results_df = get_all_evaluations()

if not all_results_df.empty:
    # Improve display
    all_results_df['evaluation_date'] = pd.to_datetime(all_results_df['evaluation_date']).dt.strftime('%Y-%m-%d %H:%M')
    all_results_df = all_results_df.sort_values(by="relevance_score", ascending=False)
    st.dataframe(all_results_df, use_container_width=True)
else:
    st.info("No evaluations have been run yet. Use the controls in the sidebar to start.")