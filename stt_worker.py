#!/usr/bin/env python
"""
stt_worker.py
-------------
External speech-to-text worker for Ren'Py.
Robust Version: Works with OR without an API Key.
"""

import sys
import json
import argparse
import traceback
import os

# --- 1. SAFE IMPORT FOR DOTENV ---
# If user doesn't have python-dotenv installed, we just skip it.
try:
    from dotenv import load_dotenv
except ImportError:
    load_dotenv = None

try:
    import speech_recognition as sr
except ImportError:
    sys.stdout.write(json.dumps({
        "ok": False,
        "text": None,
        "error": "SpeechRecognition module not installed."
    }) + "\n")
    sys.exit(1)


def get_api_key():
    """
    Safely attempts to load the GOOGLE_API_KEY.
    Returns: 
        - String (The Key) if found.
        - None if not found (Triggers default behavior).
    """
    api_key = None
    
    # Only try loading if the library exists
    if load_dotenv:
        try:
            # Find .env in the same folder as this script
            current_dir = os.path.dirname(os.path.abspath(__file__))
            env_path = os.path.join(current_dir, ".env")
            
            # Load it (silently fails if file doesn't exist)
            load_dotenv(env_path)
            
            # Get variable
            raw_key = os.getenv("GOOGLE_API_KEY")
            
            # Clean it up (remove spaces)
            if raw_key and raw_key.strip():
                api_key = raw_key.strip()
                
        except Exception:
            # If anything goes wrong reading the file, just ignore it 
            # and return None so the script keeps running.
            pass
            
    return api_key


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--lang", default="id-ID", help="Language code")
    parser.add_argument("--timeout", type=float, default=8.0)
    parser.add_argument("--phrase-time-limit", type=float, default=7.0)
    parser.add_argument("--device-index", type=int, default=None)
    args = parser.parse_args()

    # --- 2. GET KEY (OR NONE) ---
    google_key = get_api_key()

    r = sr.Recognizer()

    # --- 3. SETUP MICROPHONE ---
    try:
        if args.device_index is not None:
            source = sr.Microphone(device_index=args.device_index)
        else:
            source = sr.Microphone()
    except Exception as e:
        sys.stdout.write(json.dumps({
            "ok": False,
            "text": None,
            "error": f"Microphone error: {e}"
        }) + "\n")
        return

    # --- 4. LISTEN ---
    with source:
        try:
            r.adjust_for_ambient_noise(source, duration=1.0)
            audio = r.listen(source, timeout=args.timeout, phrase_time_limit=args.phrase_time_limit)
        except Exception as e:
            sys.stdout.write(json.dumps({
                "ok": False,
                "text": None,
                "error": f"Listening error: {e}"
            }) + "\n")
            return

    # --- 5. RECOGNIZE (ROBUST) ---
    try:
        # NOTE: 
        # If google_key is 'None', the library automatically uses 
        # the default public generic key. It will STILL work.
        text = r.recognize_google(audio, language=args.lang, key=google_key)
        
        sys.stdout.write(json.dumps({
            "ok": True,
            "text": text,
            "error": None
        }) + "\n")

    except sr.UnknownValueError:
        sys.stdout.write(json.dumps({
            "ok": False,
            "text": None,
            "error": "Speech not understood"
        }) + "\n")
    except sr.RequestError as e:
        # Specific error handling
        error_msg = str(e)
        if "quota" in error_msg.lower():
            sys.stdout.write(json.dumps({
                "ok": False,
                "text": None,
                "error": "API Quota Exceeded (Try adding a custom API Key)"
            }) + "\n")
        else:
            sys.stdout.write(json.dumps({
                "ok": False,
                "text": None,
                "error": f"Connection/API error: {e}"
            }) + "\n")
    except Exception:
        sys.stdout.write(json.dumps({
            "ok": False,
            "text": None,
            "error": "Unexpected: " + traceback.format_exc()
        }) + "\n")


if __name__ == "__main__":
    main()