import sys
import json
import os
from google import genai 
from dotenv import load_dotenv
import logging

import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

# Set log level to ERROR to hide INFO and WARNING messages
os.environ["GRPC_VERBOSITY"] = "ERROR"
os.environ["GLOG_minloglevel"] = "2"

# Also silence the standard python logger for the library
logging.getLogger('google.generativeai').setLevel(logging.ERROR)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE_DIR, ".env.gemini"))

API_KEY = os.getenv("GEMINI_API_KEY")

# Initialize the new Client
client = genai.Client(api_key=API_KEY)

def main():
    if len(sys.argv) < 2:
        print(json.dumps({"ok": False, "error": "Pertanyaan kosong"}))
        return

    question = sys.argv[1]

    try:
        # New syntax for generating content
        response = client.models.generate_content(
            model="gemini-2.0-flash", 
            contents=question,
            config={
                # --- UPDATED INSTRUCTION FOR BILINGUAL SUPPORT ---
                "system_instruction": (
                    "You are an educational assistant for children. "
                    "Topics allowed: natural disasters, safety, and mitigation only. "
                    "IMPORTANT: You must adapt to the language of the user's prompt. "
                    "1. If the prompt is in English, answer in simple, short English. "
                    "2. If the prompt is in Indonesian, answer in simple, short Indonesian. "
                    "Do not be scary. Keep explanations concise and friendly."
                ),
                # -------------------------------------------------
                "temperature": 0.4,
                "max_output_tokens": 2000,
            }
        )

        print(json.dumps({
            "ok": True,
            "question": question,
            "answer": response.text.strip()
        }, ensure_ascii=False))

    except Exception as e:
        print(json.dumps({"ok": False, "error": str(e)}))

if __name__ == "__main__":
    main()