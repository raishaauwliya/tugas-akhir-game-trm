import sys
import json
import os
from google import genai # Note the change here
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
            model="gemini-2.0-flash", # Use a valid model name
            contents=question,
            config={
                "system_instruction": (
                    "Kamu adalah asisten edukasi untuk anak-anak di Indonesia. "
                    "Topik yang boleh dibahas HANYA seputar bencana alam, "
                    "keselamatan diri, dan mitigasi bencana. "
                    "Gunakan bahasa Indonesia yang sederhana, singkat, "
                    "dan tidak menakutkan."
                ),
                "temperature": 0.4,
                "max_output_tokens": 1000,
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