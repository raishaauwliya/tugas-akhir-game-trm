#!/usr/bin/env python
"""
stt_worker.py
-------------
External speech-to-text worker for Ren'Py.

- Uses SpeechRecognition + microphone.
- Prints a single JSON line to stdout:
    {"ok": true, "text": "...", "error": null}
  or
    {"ok": false, "text": null, "error": "message"}
"""

import sys
import json
import argparse
import traceback

try:
    import speech_recognition as sr
except ImportError:
    # Fatal: SpeechRecognition tidak ada
    sys.stdout.write(json.dumps({
        "ok": False,
        "text": None,
        "error": "SpeechRecognition module not installed in this Python."
    }) + "\n")
    sys.exit(1)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--lang", default="id-ID", help="Language code, e.g. id-ID or en-US")
    parser.add_argument("--timeout", type=float, default=8.0, help="Max seconds waiting for speech start")
    parser.add_argument("--phrase-time-limit", type=float, default=7.0, help="Max seconds for phrase length")
    parser.add_argument("--device-index", type=int, default=None, help="Microphone device index (optional)")
    args = parser.parse_args()

    r = sr.Recognizer()

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

    with source:
        try:
            # Sedikit kalibrasi noise
            r.adjust_for_ambient_noise(source, duration=1.0)

            # Dengarkan 1 kalimat
            audio = r.listen(source, timeout=args.timeout, phrase_time_limit=args.phrase_time_limit)
        except Exception as e:
            sys.stdout.write(json.dumps({
                "ok": False,
                "text": None,
                "error": f"Listening error: {e}"
            }) + "\n")
            return

    # Recognize via Google Web Speech API
    try:
        text = r.recognize_google(audio, language=args.lang)
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
        sys.stdout.write(json.dumps({
            "ok": False,
            "text": None,
            "error": f"API request error: {e}"
        }) + "\n")
    except Exception:
        sys.stdout.write(json.dumps({
            "ok": False,
            "text": None,
            "error": "Unexpected error: " + traceback.format_exc()
        }) + "\n")


if __name__ == "__main__":
    main()
