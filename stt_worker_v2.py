#!/usr/bin/env python
"""
stt_worker_v2.py
-------------
SERVICE ACCOUNT VERSION FOR GOOGLE STT V2 (CHIRP)
- Uses Service Account JSON for Authentication (Required for V2 Resources).
- Fixes 403 Permission Denied & 400 Location Error.
"""

import sys
import json
import os

# --- 1. CRITICAL IMPORTS ---
try:
    import speech_recognition as sr
except ImportError:
    sys.stdout.write('{"ok": false, "error": "Missing speech_recognition"}\n')
    sys.exit(1)

# --- 2. CONFIG LOAD ---
def load_config():
    env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")
    
    # 1. Load .env manual
    if os.path.exists(env_path):
        try:
            with open(env_path, "r") as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith("#") or "=" not in line: continue
                    k, v = line.split("=", 1)
                    k, v = k.strip(), v.strip()
                    if (v.startswith('"') and v.endswith('"')) or (v.startswith("'") and v.endswith("'")):
                        v = v[1:-1]
                    os.environ[k] = v
        except: pass

load_config()

# --- 3. ARG PARSE ---
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

# --- 4. RECORDING ---
try:
    r = sr.Recognizer()
    r.energy_threshold = 300
    r.dynamic_energy_threshold = False
    r.pause_threshold = 0.6
    r.non_speaking_duration = 0.5

    if device_idx is not None:
        source = sr.Microphone(device_index=device_idx)
    else:
        source = sr.Microphone()

    with source:
        debug_log(f"LISTENING ({lang_code})...")
        audio = r.listen(source, timeout=timeout, phrase_time_limit=phrase_limit)
        debug_log("Captured.")

except Exception as e:
    sys.stdout.write(json.dumps({"ok": False, "error": f"Mic Error: {e}"}) + "\n")
    sys.exit(0)

# --- 5. AUTHENTICATION (SERVICE ACCOUNT) ---
def get_auth_token():
    """
    Mendapatkan Access Token menggunakan Service Account JSON.
    Membutuhkan: pip install google-auth requests
    """
    debug_log("Authenticating...")
    import google.auth
    import google.auth.transport.requests
    
    try:
        # Load credentials dari environment variable GOOGLE_APPLICATION_CREDENTIALS
        creds, project = google.auth.default(scopes=["https://www.googleapis.com/auth/cloud-platform"])
        
        # Refresh token untuk mendapatkan string token terbaru
        auth_req = google.auth.transport.requests.Request()
        creds.refresh(auth_req)
        
        return creds.token, project
    except Exception as e:
        return None, str(e)

# --- 6. PROCESS V2 ---
def process_v2(audio, token, project_id, recognizer_id):
    import requests
    import base64

    # LOKASI PENTING: asia-southeast1
    location = "asia-southeast1" 
    api_endpoint = f"{location}-speech.googleapis.com"
    
    debug_log(f"Sending to {api_endpoint}...")

    try:
        wav_data = audio.get_wav_data()
        content = base64.b64encode(wav_data).decode("utf-8")

        url = f"https://{api_endpoint}/v2/projects/{project_id}/locations/{location}/recognizers/{recognizer_id}:recognize"
        
        # Header menggunakan Bearer Token (bukan API Key lagi)
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "X-Goog-User-Project": project_id
        }

        payload = {
            "config": { "autoDecodingConfig": {} },
            "content": content
        }

        resp = requests.post(url, json=payload, headers=headers, timeout=15)

        if resp.status_code != 200:
            return None, f"Google V2 Error {resp.status_code}: {resp.text}"

        data = resp.json()
        if "results" in data and len(data["results"]) > 0:
            result = data["results"][0]
            if "alternatives" in result:
                return result["alternatives"][0]["transcript"], None
        
        return "", None

    except Exception as e:
        return None, str(e)

# --- 7. MAIN EXECUTION ---
# Load settings
recog_map = {
    "id-ID": os.getenv("RECOGNIZER_ID_INDO", "chirp-id"),
    "en-US": os.getenv("RECOGNIZER_ID_ENGLISH", "chirp-en")
}
target_recog = recog_map.get(lang_code, recog_map["id-ID"])

# Get Token (Auth)
token, project_err = get_auth_token()

if not token:
    # Jika gagal auth, kembalikan error JSON
    err_msg = f"Auth Error: {project_err} (Check service_account.json path)"
    sys.stdout.write(json.dumps({"ok": False, "text": None, "error": err_msg}) + "\n")
else:
    # Get Project ID from .env (or from auth if needed, but .env is safer)
    project_id = os.getenv("GOOGLE_PROJECT_ID")
    
    # Process
    text, err = process_v2(audio, token, project_id, target_recog)
    sys.stdout.write(json.dumps({"ok": not err, "text": text, "error": err}) + "\n")