from sklearn.feature_extraction.text import TfidfVectorizer
import spacy
import re

# Load the spaCy model, which is pre-installed via requirements.txt
nlp = spacy.load("en_core_web_sm")

def preprocess_text(text):
    """
    Cleans and lemmatizes text for better matching.
    """
    # Remove special characters and digits
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    doc = nlp(text.lower())
    lemmatized_tokens = [token.lemma_ for token in doc if not token.is_stop and not token.is_punct]
    return " ".join(lemmatized_tokens)


def perform_hard_match(jd_text, resume_text, num_keywords=20):
    """
    Performs a keyword match using TF-IDF.
    Returns a score (0-100), the matched keywords, and the missing keywords.
    """
    if not jd_text or not resume_text:
        return 0, [], []

    # Preprocess both texts
    processed_jd = preprocess_text(jd_text)
    processed_resume = preprocess_text(resume_text)

    # Use TF-IDF to find the most important keywords from the Job Description
    vectorizer = TfidfVectorizer()
    try:
        tfidf_matrix = vectorizer.fit_transform([processed_jd])
        feature_names = vectorizer.get_feature_names_out()
        
        # Get scores for each word
        scores = tfidf_matrix.toarray().flatten()
        
        # Create a dictionary of word -> score
        word_scores = {word: score for word, score in zip(feature_names, scores)}
        
        # Sort by score and get the top N keywords
        sorted_word_scores = sorted(word_scores.items(), key=lambda x: x[1], reverse=True)
        top_keywords = [word for word, score in sorted_word_scores[:num_keywords]]

    except ValueError:
        # Happens if the JD is too short or has no meaningful words
        return 0, [], []


    # Check which keywords are present in the resume
    found_keywords = []
    missing_keywords = []
    resume_words = set(processed_resume.split())

    for keyword in top_keywords:
        if keyword in resume_words:
            found_keywords.append(keyword)
        else:
            missing_keywords.append(keyword)

    # Calculate score
    if not top_keywords:
        return 0, [], []
        
    score = (len(found_keywords) / len(top_keywords)) * 100
    
    return score, found_keywords, missing_keywords