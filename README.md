# Automated Resume Relevance Check System

**A Submission for the Code4Edtech Challenge by Innomatics Research Labs**

---

## 🚀 Live Demo & Presentation

* **Live Application URL:** []
* **Video Walkthrough URL:** [**<< PASTE YOUR YOUTUBE VIDEO URL HERE >>**]

---

## 1. Problem Statement

At Innomatics Research Labs, the placement team manually evaluates thousands of resumes against 18-20 new job descriptions weekly.This manual process is time-consuming, inconsistent, and leads to significant delays in shortlisting candidates. The objective of this project is to build an automated system that can evaluate resume relevance at scale, provide consistent scoring, and offer actionable feedback.

## 2. Our Approach

To solve this problem, we developed a multi-page Streamlit application powered by the Google Gemini API. Our approach is centered around a **Hybrid Scoring Engine** that combines the speed of traditional keyword analysis with the deep contextual understanding of modern Large Language Models.

The workflow is as follows:
1.  **Dual User Roles:** The application serves two distinct user groups: a public-facing portal for students to submit resumes and a private, password-protected dashboard for the placement team.
2.  **Resume Parsing:** Upon upload, `.pdf` and `.docx` files are parsed to extract raw text content.
3.  **Keyword Match (Hard Match):** We use a TF-IDF vectorizer to identify the most critical keywords from the job description and calculate a score based on their presence in the resume. This accounts for **50%** of the final score.
4.  **Semantic Match (Soft Match):** We use Google's `text-embedding-004` model to convert both the resume and the job description into numerical vectors. The cosine similarity between these vectors provides a score based on contextual and semantic relevance. This accounts for the remaining **50%** of the final score.
5.  **AI-Generated Feedback:** Google's `gemini-1.5-pro` model generates personalized, actionable feedback for students, highlighting missing skills and suggesting improvements.
6.  **Data Persistence:** All evaluation results are saved to a local SQLite database, which populates the admin dashboard.

This hybrid approach ensures that the final score is balanced, accurate, and not overly reliant on either exact keywords or general semantic similarity alone.

## 3. Installation Steps

To run this project locally, please follow these steps:

1.  **Clone the Repository:**
    Get your repository URL using the steps above and paste it here.
    ```bash
    git clone [https://github.com/saiteja03k/automated-resume-screener.git]
    cd automated-resume-screener
    ```
2.  **Create and Activate a Virtual Environment:**
    ```bash
    python -m venv venv
    # For Windows (PowerShell)
    .\venv\Scripts\Activate.ps1
    ```
3.  **Install All Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
4.  **Set Up Your Environment Variable:**
    You will need a Google Gemini API key. Set it in your terminal:
    ```bash
    # For Windows (PowerShell)
    $env:GEMINI_API_KEY = "YOUR_GEMINI_API_KEY_HERE"
    ```
5.  **Run the Application:**
    ```bash
    streamlit run Submission_Portal.py
    ```

## 4. Usage

The application has two main pages accessible from the sidebar.

#### **Submission Portal:**
This is the main page for students or for batch-uploading.
1.  Paste a job description into the text area or upload a JD file.
2.  Click "Browse files" to upload one or more resumes (`.pdf` or `.docx`).
3.  Click the "Analyze Resumes" button.
4.  The results, including the relevance score, verdict, and AI feedback, will appear on the screen for each resume.

#### **Admin Dashboard:**
This page is for the placement team.
1.  Navigate to the "Admin Dashboard" page from the sidebar.
2.  You will be prompted to enter a password in the sidebar. The password is: `admin123`
3.  Upon entering the correct password, the dashboard will load, showing a table of all historical evaluations.
4.  Use the filters in the sidebar to search the results by Job Title, Verdict, or Score Range.