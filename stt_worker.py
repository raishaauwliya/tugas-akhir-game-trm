#!/usr/bin/env python
"""
stt_worker.py
-------------
ULTRA-LOW LATENCY VERSION
- Lazy Imports: Library berat (requests, base64) baru di-load SETELAH merekam.
- Mic menyala secepat mungkin untuk menghindari kalimat terpotong.
"""

import sys
import json
import argparse
import os

# --- GLOBAL DEBUG ---
DEBUG_MODE = False

def debug_log(msg):
    if DEBUG_MODE:
        sys.stderr.write(f"[DEBUG] {msg}\n")
        sys.stderr.flush()

# Import ini wajib di awal agar bisa akses Mic
try:
    import speech_recognition as sr
except ImportError as e:
    sys.stdout.write(json.dumps({"ok": False, "error": f"Missing lib: {e}"}) + "\n")
    sys.exit(1)

# --- FUNGSI LOAD API KEY (Cek Env Var Saja biar Cepat) ---
def get_api_key_fast():
    # Prioritaskan Environment Variable System (Paling Cepat)
    return os.getenv("GOOGLE_API_KEY")

# --- FUNGSI PROSES (REST API) ---
def process_with_rest_api(audio, api_key, lang_code):
    debug_log("Processing: Importing heavy libs now...")
    
    # ⚡ LAZY IMPORT: Di-load hanya SETELAH rekaman selesai
    # Ini menghemat waktu startup di awal.
    import base64
    import requests 
    
    try:
        wav_data = audio.get_wav_data()
        audio_content = base64.b64encode(wav_data).decode("utf-8")

        url = "https://speech.googleapis.com/v1/speech:recognize"
        params = {"key": api_key}
        payload = {
            "config": {
                "encoding": "LINEAR16",
                "sampleRateHertz": audio.sample_rate,
                "languageCode": lang_code,
            },
            "audio": { "content": audio_content }
        }

        response = requests.post(url, params=params, json=payload, timeout=5)
        
        if response.status_code != 200:
            return None, f"Google Error {response.status_code}"

        result_json = response.json()
        if "results" in result_json:
            return result_json["results"][0]["alternatives"][0]["transcript"], None
        else:
            return "", None 
    except Exception as e:
        return None, str(e)


# --- FUNGSI PROSES (FALLBACK) ---
def process_with_library_default(audio, lang_code):
    debug_log("Processing: Fallback method...")
    r = sr.Recognizer()
    try:
        text = r.recognize_google(audio, language=lang_code, key=None)
        return text, None
    except sr.UnknownValueError:
        return "", None
    except Exception as e:
        return None, str(e)


def main():
    global DEBUG_MODE
    parser = argparse.ArgumentParser()
    parser.add_argument("--lang", default="id-ID")
    parser.add_argument("--timeout", type=float, default=5.0)
    parser.add_argument("--phrase-time-limit", type=float, default=5.0)
    parser.add_argument("--device-index", type=int, default=None)
    parser.add_argument("--debug", action="store_true")
    args = parser.parse_args()

    if args.debug: DEBUG_MODE = True

    # 1. SETUP MIC SECEPAT MUNGKIN
    r = sr.Recognizer()
    
    # Setting Sensitivitas Statis (Tanpa Kalibrasi = Instant)
    r.energy_threshold = 300  
    r.dynamic_energy_threshold = False 
    
    # Deteksi diam lebih cepat (0.4 detik diam = selesai)
    r.pause_threshold = 0.4
    r.non_speaking_duration = 0.3

    try:
        # Buka Mic
        if args.device_index is not None:
            source = sr.Microphone(device_index=args.device_index)
        else:
            source = sr.Microphone()
            
        with source:
            debug_log("LISTENING NOW (Libs loading later)...")
            
            # --- MULAI REKAM ---
            # Di titik ini, library 'requests' belum di-load.
            # Jadi kita sampai di baris ini lebih cepat (~300-500ms lebih cepat).
            audio = r.listen(source, timeout=args.timeout, phrase_time_limit=args.phrase_time_limit)
            
            debug_log("Audio Captured. Now loading libs...")

    except Exception as e:
        sys.stdout.write(json.dumps({"ok": False, "error": f"Mic Error: {e}"}) + "\n")
        return

    # 2. SELESAI REKAM -> BARU IMPORT LAIN-LAIN
    # User tidak akan sadar ada delay di sini, karena mereka sudah selesai bicara.
    
    # Coba load .env (opsional, ditaruh di sini biar gak ganggu start awal)
    api_key = get_api_key_fast()
    if not api_key:
        try:
            from dotenv import load_dotenv
            load_dotenv(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env"))
            api_key = os.getenv("GOOGLE_API_KEY")
        except:
            pass

    text_result = None
    error_msg = None

    # 3. KIRIM DATA
    if api_key:
        text_result, error_msg = process_with_rest_api(audio, api_key, args.lang)
    
    # Fallback Logic
    if (not api_key) or (error_msg and "Google Error" in error_msg):
        text_result, error_msg = process_with_library_default(audio, args.lang)

    # 4. OUTPUT
    if error_msg is not None:
        sys.stdout.write(json.dumps({"ok": False, "text": None, "error": error_msg}) + "\n")
    else:
        sys.stdout.write(json.dumps({"ok": True, "text": text_result, "error": None}) + "\n")

if __name__ == "__main__":
    main()