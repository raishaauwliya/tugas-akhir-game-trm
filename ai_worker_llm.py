# ai_llm_worker.py
import sys
import json
import os
import google.generativeai as genai

# =============================
# Konfigurasi Gemini
# =============================
API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    print(json.dumps({
        "ok": False,
        "error": "GEMINI_API_KEY tidak ditemukan"
    }))
    sys.exit(1)

genai.configure(api_key=API_KEY)

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    system_instruction=(
        "Kamu adalah asisten edukasi untuk anak-anak di Indonesia. "
        "Topik yang boleh dibahas HANYA seputar:\n"
        "- Bencana alam (banjir, longsor, gempa, tsunami, gunung api)\n"
        "- Keselamatan diri dan lingkungan\n"
        "- Evakuasi dan kesiapsiagaan bencana\n\n"
        "Gunakan bahasa Indonesia yang sederhana, singkat, "
        "tidak menakutkan, dan mudah dipahami anak."
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
                "max_output_tokens": 200
            }
        )

        answer = response.text.strip()

        print(json.dumps({
            "ok": True,
            "question": question,
            "answer": answer
        }))

    except Exception as e:
        print(json.dumps({
            "ok": False,
            "error": str(e)
        }))

if __name__ == "__main__":
    main()
