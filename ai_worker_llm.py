import sys
import json
import os
import time
import io  # <--- Required for the encoding fix
import logging
import warnings
from google import genai
from dotenv import load_dotenv

# ==========================================
# 1. FIX FOR WINDOWS EMOJI ERROR (CRITICAL)
# ==========================================
# This forces Python to use UTF-8 for output, ensuring emojis don't crash the script.
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# --- CONFIGURATION ---
MAX_RETRIES = 3
INITIAL_DELAY = 2  # Seconds

warnings.filterwarnings("ignore", category=DeprecationWarning)

# Set log level to ERROR
os.environ["GRPC_VERBOSITY"] = "ERROR"
os.environ["GLOG_minloglevel"] = "2"
logging.getLogger('google.generativeai').setLevel(logging.ERROR)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE_DIR, ".env.gemini"))

API_KEY = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=API_KEY)

def generate_with_retry(question):
    delay = INITIAL_DELAY
    
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            response = client.models.generate_content(
                model="gemini-2.0-flash", 
                contents=question,
                config={
                    "system_instruction": (
                        "You are an educational assistant for children. "
                        "Topics allowed: natural disasters, safety, and mitigation only. "
                        "IMPORTANT: You must adapt to the language of the user's prompt. "
                        "1. If the prompt is in English, answer in simple, short English. "
                        "2. If the prompt is in Indonesian, answer in simple, short Indonesian. "
                        "Do not be scary. Keep explanations concise and friendly."
                    ),
                    "temperature": 0.4,
                    "max_output_tokens": 1000,
                }
            )
            return response.text.strip()

        except Exception as e:
            error_str = str(e).lower()
            # Retry on 429 (Rate Limit) or 503 (Server Overload)
            if "429" in error_str or "resource exhausted" in error_str or "quota" in error_str or "503" in error_str:
                if attempt < MAX_RETRIES:
                    # Wait and retry
                    time.sleep(delay)
                    delay *= 2  # Exponential backoff (2s -> 4s -> 8s)
                    continue
                else:
                    raise Exception("Server is busy. Please try again later.")
            else:
                # If it's a real error (like Invalid API Key), fail immediately
                raise e

def main():
    if len(sys.argv) < 2:
        print(json.dumps({"ok": False, "error": "Pertanyaan kosong"}))
        return

    question = sys.argv[1]

    try:
        answer = generate_with_retry(question)
        
        print(json.dumps({
            "ok": True,
            "question": question,
            "answer": answer
        }, ensure_ascii=False))

    except Exception as e:
        # If an error occurs, print it safely as JSON
        print(json.dumps({"ok": False, "error": str(e)}))

if __name__ == "__main__":
    main()