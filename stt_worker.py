#!/usr/bin/env python
"""
stt_worker.py
-------------
BARE METAL VERSION
- Removed 'argparse' (heavy) -> Uses manual argument parsing.
- Removed 'traceback' & 'os' from startup.
- Absolute minimal code before recording starts.
"""

import sys
import json

# --- 1. CRITICAL IMPORTS ONLY ---
try:
    import speech_recognition as sr
except ImportError as e:
    sys.stdout.write('{"ok": false, "error": "Missing speech_recognition"}\n')
    sys.exit(1)

# --- 2. FAST MANUAL ARGUMENT PARSING ---
# We avoid argparse to save startup time.
# Defaults:
lang_code = "id-ID"
timeout = 15.0
phrase_limit = 14.0
device_idx = None
debug_mode = False

args = sys.argv[1:]
for i, arg in enumerate(args):
    if arg == "--lang" and i+1 < len(args):
        lang_code = args[i+1]
    elif arg == "--debug":
        debug_mode = True
    elif arg == "--device-index" and i+1 < len(args):
        try: device_idx = int(args[i+1])
        except: pass

def debug_log(msg):
    if debug_mode:
        sys.stderr.write(f"[DEBUG] {msg}\n")
        sys.stderr.flush()

# --- 3. INSTANT RECORDING START ---
try:
    r = sr.Recognizer()
    
    # HARDCODED OPTIMIZATION (No dynamic calculation)
    r.energy_threshold = 300
    r.dynamic_energy_threshold = False
    r.pause_threshold = 0.6
    r.non_speaking_duration = 0.5

    # Open Mic
    if device_idx is not None:
        source = sr.Microphone(device_index=device_idx)
    else:
        source = sr.Microphone()

    with source:
        debug_log("LISTENING (Bare Metal)...")
        # ⚡ THE MOMENT OF TRUTH
        audio = r.listen(source, timeout=timeout, phrase_time_limit=phrase_limit)
        debug_log("Captured.")

except Exception as e:
    # Manual JSON construction is faster than loading json library for simple errors? 
    # No, we kept json imported. It's fine.
    sys.stdout.write(json.dumps({"ok": False, "error": f"Mic Error: {e}"}) + "\n")
    sys.exit(0)

# --- 4. LAZY LOAD EVERYTHING ELSE ---
# The user has stopped speaking. Now we load the heavy internet tools.
import os

def get_api_key_fast():
    # 1. System Env (Fastest)
    key = os.getenv("GOOGLE_API_KEY")
    if key: return key
    
    # 2. .env file (Slower, only if needed)
    try:
        from dotenv import load_dotenv
        load_dotenv(os.path.join(os.path.dirname(os.path.abspath(_file_)), ".env"))
        return os.getenv("GOOGLE_API_KEY")
    except:
        return None

def process_rest(audio, key, lang):
    debug_log("Loading REST libs...")
    import requests
    import base64
    
    try:
        wav_data = audio.get_wav_data()
        content = base64.b64encode(wav_data).decode("utf-8")
        
        url = "https://speech.googleapis.com/v1/speech:recognize"
        params = {"key": key}
        payload = {
            "config": {
                "encoding": "LINEAR16", 
                "sampleRateHertz": audio.sample_rate, 
                "languageCode": lang
            },
            "audio": {"content": content}
        }
        
        resp = requests.post(url, params=params, json=payload, timeout=5)
        if resp.status_code != 200: return None, f"Google Error {resp.status_code}"
        
        data = resp.json()
        if "results" in data:
            return data["results"][0]["alternatives"][0]["transcript"], None
        return "", None
    except Exception as e:
        return None, str(e)

def process_fallback(audio, lang):
    debug_log("Fallback...")
    try:
        return r.recognize_google(audio, language=lang, key=None), None
    except Exception as e:
        return None, str(e)

# --- 5. EXECUTION ---
api_key = get_api_key_fast()
text = None
err = None

if api_key:
    text, err = process_rest(audio, api_key, lang_code)

if (not api_key) or (err and "Google" in err):
    text, err = process_fallback(audio, lang_code)

# Output
sys.stdout.write(json.dumps({"ok": not err, "text": text, "error": err}) + "\n")