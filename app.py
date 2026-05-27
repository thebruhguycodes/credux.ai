import streamlit as st
from google import genai
from pypdf import PdfReader

# Page Configuration
st.set_page_config(page_title="Credux.ai", page_icon="🛡️", layout="wide")

st.title("🛡️ Credux.ai")
st.subheader("Automated Enterprise Compliance & Documentation Vetting")

# Sidebar for API Key
with st.sidebar:
    st.header("Authentication")
    api_key = st.text_input("Enter Gemini API Key", type="password")

# Document Analysis
uploaded_file = st.file_uploader("Upload vendor PDF", type=["pdf"])

if st.button("Run Credux Vetting Engine"):
    if not api_key:
        st.error("Please enter your Gemini API Key in the sidebar.")
    elif not uploaded_file:
        st.error("Please upload a PDF file.")
    else:
        with st.spinner("Analyzing document..."):
            try:
                # 1. Extract text from PDF
                reader = PdfReader(uploaded_file)
                document_text = "\n".join([page.extract_text() for page in reader.pages if page.extract_text()])
                
                # 2. Initialize Client and Generate Content
                client = genai.Client(api_key=api_key)
                prompt = f"Analyze this document for legal and operational risks:\n\n{document_text}"
                
                response = client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=prompt
                )
                
                st.markdown("### 📋 Risk Assessment Report")
                st.write(response.text)
                
            except Exception as e:
                st.error(f"An error occurred: {e}")
