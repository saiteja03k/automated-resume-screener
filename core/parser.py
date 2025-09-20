import pypdf
import docx
import io

def extract_text_from_file(uploaded_file):
    """
    Extracts text from an uploaded file (PDF or DOCX).
    """
    if uploaded_file.name.endswith('.pdf'):
        try:
            # Use a BytesIO object to handle the uploaded file in memory
            pdf_stream = io.BytesIO(uploaded_file.getvalue())
            reader = pypdf.PdfReader(pdf_stream)
            text = ""
            for page in reader.pages:
                text += page.extract_text() or ""
            return text
        except Exception as e:
            return f"Error reading PDF file: {e}"
            
    elif uploaded_file.name.endswith('.docx'):
        try:
            # Use a BytesIO object for the docx file as well
            doc_stream = io.BytesIO(uploaded_file.getvalue())
            doc = docx.Document(doc_stream)
            text = ""
            for para in doc.paragraphs:
                text += para.text + "\n"
            return text
        except Exception as e:
            return f"Error reading DOCX file: {e}"
            
    else:
        return "Unsupported file format. Please upload a PDF or DOCX file."