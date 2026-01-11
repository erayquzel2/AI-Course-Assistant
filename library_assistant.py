import PyPDF2
import os
from google import genai

# Başarılı olan API anahtarınızı buraya koyun
API_KEY = "-YOUR_API_KEY_HERE"
client = genai.Client(api_key=API_KEY)

def get_all_pdf_text(folder_path):
    full_text = ""
    # Klasördeki tüm dosyaları tara
    for filename in sorted(os.listdir(folder_path)):
        if filename.endswith(".pdf"):
            print(f"Reading {filename}...")
            with open(os.path.join(folder_path, filename), "rb") as f:
                reader = PyPDF2.PdfReader(f)
                for page in reader.pages:
                    full_text += page.extract_text() + "\n"
    return full_text

def run_library_assistant():
    # 1. Adım: Tüm notları birleştir (PDF'lerin olduğu klasör yolunu yaz)
    folder_path = "./nyp_notlari" # PDF'lerin olduğu klasör adı
    context_data = get_all_pdf_text(folder_path)
    
    print("\n--- All notes loaded. AI is analyzing... ---\n")

    # 2. Adım: Kullanıcıdan soru al
    user_query = input("Ask anything about your OOP course: ")

    # 3. Adım: AI'ya tüm notları bağlam (context) olarak gönder
    system_instruction = (
        "You are an expert Computer Science Tutor. "
        "Use the provided course notes to answer the student's questions. "
        "Be technical but clear."
    )

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            config={'system_instruction': system_instruction},
            contents=f"COURSE NOTES:\n{context_data}\n\nSTUDENT QUESTION: {user_query}"
        )

        print("\n[AI TUTOR RESPONSE]:")
        print("-" * 30)
        print(response.text)
        print("-" * 30)

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    run_library_assistant()