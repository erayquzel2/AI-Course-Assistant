import streamlit as st
from google import genai
import PyPDF2
import io

# Sayfa yapılandırması - Profesyonel görünüm
st.set_page_config(page_title="AI Smart Tutor", page_icon="🤖", layout="centered")
st.title("🚀 Ultimate AI Study Assistant")
st.markdown("---")

# API Setup
# Success! yazısını aldığın anahtarı buraya yaz
client = genai.Client(api_key="YOUR_API_KEY_HERE")

# Sohbet hafızasını başlat
if "messages" not in st.session_state:
    st.session_state.messages = []
if "full_context" not in st.session_state:
    st.session_state.full_context = ""

# Yan Panel - Dosya Yönetimi
with st.sidebar:
    st.header("📂 Document Center")
    uploaded_files = st.file_uploader("Upload your PDF notes", type="pdf", accept_multiple_files=True)
    
    if st.button("Process & Learn"):
        if uploaded_files:
            with st.spinner("Analyzing documents..."):
                combined_text = ""
                for uploaded_file in uploaded_files:
                    pdf_reader = PyPDF2.PdfReader(uploaded_file)
                    for page in pdf_reader.pages:
                        combined_text += page.extract_text() + "\n"
                st.session_state.full_context = combined_text
                st.success(f"{len(uploaded_files)} files processed!")
        else:
            st.error("Please upload at least one PDF.")

# Ana Sohbet Ekranı
# Önceki mesajları ekrana bas
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Kullanıcıdan soru al
if prompt := st.chat_input("Ask about your notes..."):
    # Mesajı hafızaya ekle
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # AI Yanıtı üret
    with st.chat_message("assistant"):
        if st.session_state.full_context:
            with st.spinner("Thinking..."):
                # Mühendislik notu: Sisteme rol ve bağlam (context) veriyoruz
                full_prompt = f"Context from notes: {st.session_state.full_context}\n\nUser Question: {prompt}"
                
                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=full_prompt
                )
                
                ai_response = response.text
                st.markdown(ai_response)
                # Yanıtı hafızaya ekle
                st.session_state.messages.append({"role": "assistant", "content": ai_response})
        else:
            st.warning("Please upload and process your notes from the sidebar first.")