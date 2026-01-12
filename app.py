import streamlit as st
from google import genai
import PyPDF2

# Config
st.set_page_config(page_title="AI Smart Tutor", page_icon="⚡", layout="centered")
st.title("⚡ AI Study Assistant")

# Auth
try:
    client = genai.Client(api_key=st.secrets["API_KEY"])
except:
    st.error("Missing API Key in secrets.")
    st.stop()

# Optimization: Cache results to avoid reprocessing heavy files
@st.cache_data
def process_pdfs(uploaded_files):
    combined_text = ""
    for file in uploaded_files:
        try:
            reader = PyPDF2.PdfReader(file)
            for page in reader.pages:
                text = page.extract_text()
                if text:
                    combined_text += text + "\n"
        except Exception as e:
            st.warning(f"Error reading file: {e}")
    return combined_text

# Sidebar
with st.sidebar:
    st.header("📂 Document Center")
    uploaded_files = st.file_uploader("Upload PDF notes", type="pdf", accept_multiple_files=True)
    process_btn = st.button("Analyze Notes")

# Main Logic
if uploaded_files and process_btn:
    with st.spinner("Processing..."):
        text_data = process_pdfs(uploaded_files)
        st.session_state.full_context = text_data
        st.success(f"✅ {len(uploaded_files)} files cached.")

# Session State for Chat
if "messages" not in st.session_state:
    st.session_state.messages = []

# Render Chat History
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User Input Handler
if prompt := st.chat_input("Ask about your notes..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate Response
    if "full_context" in st.session_state and st.session_state.full_context:
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    # RAG Implementation
                    response = client.models.generate_content(
                        model="gemini-2.5-flash",
                        contents=f"Context:\n{st.session_state.full_context}\n\nQuestion: {prompt}"
                    )
                    st.markdown(response.text)
                    st.session_state.messages.append({"role": "assistant", "content": response.text})
                except Exception as e:
                    st.error(f"API Error: {e}")
    else:
        st.warning("Please upload and analyze PDFs first.")
