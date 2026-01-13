import sys
import json
import os
import google.generativeai as genai
from dotenv import load_dotenv

# =============================
# Load ENV
# =============================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE_DIR, ".env"))

API_KEY = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")

if not API_KEY:
    print(json.dumps({
        "ok": False,
        "error": "API key tidak ditemukan"
    }))
    sys.exit(1)

# =============================
# Konfigurasi Gemini (SDK LAMA)
# =============================
genai.configure(api_key=API_KEY)

model = genai.GenerativeModel(
    model_name="gemini-2.5-flash",
    system_instruction=(
        "Kamu adalah asisten edukasi untuk anak-anak di Indonesia. "
        "Topik yang boleh dibahas HANYA seputar bencana alam, "
        "keselamatan diri, dan mitigasi bencana. "
        "Gunakan bahasa Indonesia yang sederhana, singkat, "
        "dan tidak menakutkan."
    )
)

def main():
    if len(sys.argv) < 2:
        print(json.dumps({
            "ok": False,
            "error": "Pertanyaan kosong"
        }))
        return

    question = sys.argv[1]

    try:
        response = model.generate_content(
            question,
            generation_config={
                "temperature": 0.4,
                "max_output_tokens": 10000
            }
        )

        print(json.dumps({
            "ok": True,
            "question": question,
            "answer": response.text.strip()
        }, ensure_ascii=False))

    except Exception as e:
        print(json.dumps({
            "ok": False,
            "error": str(e)
        }))

if __name__ == "__main__":
    main()
