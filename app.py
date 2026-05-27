import streamlit as st
# Initialize the client
    client = genai.Client(api_key=api_key)
    
    # Generate content using the client
    response = client.models.generate_content(
        model='gemini-2.5-flash', 
        contents=prompt
    )
from pypdf import PdfReader

# Page Configuration with Credux Branding
st.set_page_config(
    page_title="Credux.ai | Enterprise Risk & Vendor Vetting",
    page_icon="🛡️",
    layout="wide"
)

# Custom styling to mimic a sleek, minimalist dark UI
st.markdown("""
    <style>
    .main { background-color: #0d1117; color: #ffffff; }
    h1, h2, h3 { color: #b19ffb !important; font-family: 'sans-serif'; }
    .stButton>button { background-color: #6366f1; color: white; border-radius: 8px; }
    </style>
""", unsafe_allow_html=True)

st.title("🛡️ Credux.ai")
st.subheader("Automated Enterprise Compliance & Documentation Vetting")

# Sidebar for API Key validation
with st.sidebar:
    st.header("Authentication")
    api_key = st.text_input("Enter Gemini API Key", type="password")
    st.markdown("---")
    st.markdown("🔒 *Private Cloud Execution Engine*")

# Main Dashboard Tabs
tab1, tab2 = st.tabs(["📄 Document Analysis", "📊 Risk Ledger"])

with tab1:
    st.write("Upload vendor contracts, certifications, or regulatory documentation to run a live risk analysis.")
    uploaded_file = st.file_uploader("Drag and drop vendor PDF here", type=["pdf"])
    
    if uploaded_file and api_key:
        st.success("Document uploaded successfully. Ready to run analysis.")
        if st.button("Run Credux Vetting Engine"):
            with st.spinner("Analyzing document architecture and tracking risk vectors..."):
                # Initialize the Gemini client configuration
                try:
                    genai.configure(api_key=api_key)
                    model = genai.GenerativeModel('gemini-2.5-flash')
                    
                    # Extract text from the uploaded PDF
                    reader = PdfReader(uploaded_file)
                    document_text = ""
                    for page in reader.pages:
                        text = page.extract_text()
                        if text:
                            document_text += text
                    
                    # Analyze text if successfully extracted
                    if document_text.strip():
                        prompt = f"Analyze the following corporate documentation for compliance errors, structural legal risks, and operational vulnerabilities. Highlight key risk items clearly:\n\n{document_text}"
                        response = model.generate_content(prompt)
                        st.markdown("### 📋 Risk Assessment Report")
                        st.write(response.text)
                    else:
                        st.error("Could not extract legible text from the PDF. Please check file formatting.")
                except Exception as e:
                    st.error(f"Execution Error: {str(e)}")
    elif uploaded_file and not api_key:
        st.info("Please provide your Gemini API key in the sidebar to authorize the AI engine.")

with tab2:
    st.write("Historical compliance tracking and systemic enterprise risk logs will generate here.")
    
