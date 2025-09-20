import streamlit as st
import os

# Import your custom modules
from core.parser import extract_text_from_file
from core.matcher import perform_hard_match
from core.scoring import get_embedding, perform_semantic_match, calculate_final_score, get_verdict, generate_feedback
from utils.db_utils import create_table, save_evaluation

# --- Page Configuration ---
st.set_page_config(
    page_title="Resume Submission Portal",
    page_icon="📄",
    layout="wide"
)

# --- Main Application Logic ---

# Check for API Key
if "GEMINI_API_KEY" not in os.environ:
    st.error("🚨 Gemini API Key not found! Please ensure it is configured in the Streamlit secrets.")
    st.stop()

# Initialize the database and table
create_table()

# --- UI Layout ---
st.title("👨‍🎓 Student Resume Submission Portal")
st.markdown("Select a Job Description and upload your resume to get an instant relevance score and feedback.")

# --- Job Description and Resume Input ---
col1, col2 = st.columns(2)

with col1:
    st.subheader("1. Job Description")
    jd_text = st.text_area("Paste the Job Description here", height=300)

with col2:
    st.subheader("2. Upload Your Resume")
    uploaded_file = st.file_uploader(
        "Choose a resume file (PDF or DOCX)", 
        type=['pdf', 'docx'], 
        accept_multiple_files=False # Students submit one resume at a time
    )

analyze_button = st.button("Analyze My Resume", use_container_width=True, type="primary")

# --- Analysis and Results ---
if analyze_button:
    if not jd_text:
        st.warning("Please paste a Job Description.")
    elif not uploaded_file:
        st.warning("Please upload your resume.")
    else:
        with st.spinner("Analyzing your resume... This may take a moment. 🧠"):
            # Process Job Description
            jd_embedding = get_embedding(jd_text)
            
            if jd_embedding is None:
                st.error("Could not process the Job Description. It might be too short or an API error occurred.")
                st.stop()

            # Process Resume
            st.markdown(f"---")
            st.subheader(f"Analysis for: `{uploaded_file.name}`")
            
            resume_text = extract_text_from_file(uploaded_file)
            
            hard_match_score, found, missing = perform_hard_match(jd_text, resume_text)
            resume_embedding = get_embedding(resume_text)
            semantic_score = perform_semantic_match(jd_embedding, resume_embedding)
            final_score = calculate_final_score(hard_match_score, semantic_score)
            verdict = get_verdict(final_score)
            feedback = generate_feedback(jd_text, resume_text, missing)

            # Save to Database
            job_title_placeholder = " ".join(jd_text.split()[:5]) + "..."
            save_evaluation(job_title_placeholder, uploaded_file.name, final_score, verdict, missing, feedback)

            # Display Results
            st.success("Analysis Complete!")
            col1, col2, col3 = st.columns(3)
            col1.metric("Relevance Score", f"{final_score}%", delta=verdict)
            col2.metric("Keyword Match", f"{int(hard_match_score)}%")
            col3.metric("Semantic Match", f"{int(semantic_score)}%")

            with st.expander("Show AI Feedback and Missing Keywords"):
                st.markdown("##### AI-Generated Feedback for Improvement")
                st.info(feedback)
                st.markdown("##### Missing Keywords")
                st.warning(", ".join(missing) if missing else "None")