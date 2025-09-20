import google.generativeai as genai
import os
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

# Configure the Gemini API
try:
    genai.configure(api_key=os.environ["GEMINI_API_KEY"])
except KeyError:
    # This will be handled in the Streamlit app with a proper message
    pass

def get_embedding(text):
    """
    Generates an embedding for a given text using Gemini.
    """
    try:
        processed_text = text.replace("\n", " ")
        result = genai.embed_content(
            model="models/text-embedding-004",
            content=processed_text,
            task_type="RETRIEVAL_DOCUMENT"
        )
        return result['embedding']
    except Exception as e:
        print(f"Error creating embedding: {e}")
        return None

def perform_semantic_match(jd_embedding, resume_embedding):
    """
    Calculates cosine similarity and normalizes it to a 0-100 score.
    """
    if jd_embedding is None or resume_embedding is None:
        return 0

    jd_embedding = np.array(jd_embedding).reshape(1, -1)
    resume_embedding = np.array(resume_embedding).reshape(1, -1)
    
    sim_score = cosine_similarity(jd_embedding, resume_embedding)[0][0]
    
    # Normalize from [-1, 1] to [0, 100]
    normalized_score = ((sim_score + 1) / 2) * 100
    return normalized_score

def calculate_final_score(hard_match_score, semantic_match_score):
    """
    Calculates the final weighted score.
    """
    # NEW Weights: 60% for hard match, 40% for semantic match
    final_score = (0.6 * hard_match_score) + (0.4 * semantic_match_score)
    return int(final_score)

def get_verdict(score):
    """
    Determines the verdict based on the final score.
    """
    if score >= 70: # Lowered the bar for a "High" verdict
        return "High"
    elif 50 <= score < 70: # Adjusted the "Medium" range
        return "Medium"
    else:
        return "Low"

def generate_feedback(jd_text, resume_text, missing_skills):
    """
    [cite_start]Generates personalized feedback using Gemini Pro. [cite: 113]
    """
    model = genai.GenerativeModel('gemini-1.5-pro-latest')
    
    # Create a concise list of missing skills for the prompt
    missing_skills_str = ", ".join(missing_skills[:5]) # Show top 5 missing

    prompt = f"""
    As an expert career coach for Innomatics Research Labs, provide constructive, personalized feedback for a student.
    The feedback should be encouraging and offer 2-3 actionable suggestions for improving their resume based on the identified gaps.
    Keep the feedback concise and to the point.

    **Job Description Keywords:**
    {jd_text[:800]}

    **Resume Snippet:**
    {resume_text[:800]}

    **Identified Missing Keywords in Resume:**
    {missing_skills_str}

    **Constructive Feedback:**
    """
    
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Could not generate feedback due to an API error: {e}"