#!/usr/bin/env python3
"""
Real-time CLI Speech Transcriber (English / Indonesian)
------------------------------------------------------
- Uses the microphone and Google Web Speech API via the `SpeechRecognition` library.
- Lets you choose English (en-US) or Indonesian (id-ID) at startup.
- Prints transcriptions to the terminal as you speak (short phrases).

Usage:
    python realtime_transcribe_cli.py
    # Then follow the on-screen prompt to select language.
    
Stop:
    Press Ctrl+C to stop listening and exit.
"""
import sys
import time
import queue
import threading
from datetime import datetime

try:
    import speech_recognition as sr
except ImportError:
    print("Error: The 'speechrecognition' package is not installed.\n"
          "Install it with:\n    pip install SpeechRecognition pyaudio\n"
          "On Linux, you may need system libs for PortAudio: e.g., 'sudo apt install portaudio19-dev'")
    sys.exit(1)


LANG_OPTIONS = {
    "1": ("English (US)", "en-US"),
    "2": ("Bahasa Indonesia", "id-ID"),
}


def prompt_language() -> str:
    print("=== Real-time CLI Speech Transcriber ===")
    print("Choose language:")
    for k, (label, code) in LANG_OPTIONS.items():
        print(f"  {k}. {label} [{code}]")
    choice = input("Enter 1 or 2 (default 1): ").strip() or "1"
    if choice not in LANG_OPTIONS:
        print("Invalid choice, defaulting to English (US).")
        choice = "1"
    label, code = LANG_OPTIONS[choice]
    print(f"→ Using language: {label} ({code})\n")
    return code


def print_header():
    print("Tips:")
    print(" - Speak clearly near your microphone.")
    print(" - Background noise is reduced by calibration on start.")
    print(" - Transcriptions will appear below in short chunks.")
    print(" - Press Ctrl+C to stop.\n")
    print("Listening...\n")


def main():
    lang_code = prompt_language()
    r = sr.Recognizer()
    # Lower energy threshold reacts to softer speech; adjust dynamically.
    r.dynamic_energy_threshold = True

    # Select the default system microphone (you can change device_index if needed)
    try:
        mic = sr.Microphone()
    except OSError as e:
        print("Could not access the default microphone. If you have multiple devices, "
              "specify a device_index in sr.Microphone(device_index=...).")
        print(f"Microphone error: {e}")
        sys.exit(2)

    with mic as source:
        # Calibrate the energy threshold for ambient noise
        print("Calibrating microphone for ambient noise (1.5s)...")
        r.adjust_for_ambient_noise(source, duration=1.5)
        print(f"Calibration done. Energy threshold: {r.energy_threshold:.1f}\n")

    # We'll collect errors and messages from the background thread safely
    msg_queue: "queue.Queue[str]" = queue.Queue()

    def callback(recognizer: sr.Recognizer, audio: sr.AudioData):
        """Called from a background thread whenever a phrase is captured."""
        try:
            text = recognizer.recognize_google(audio, language=lang_code)
            timestamp = datetime.now().strftime("%H:%M:%S")
            msg_queue.put(f"[{timestamp}] {text}")
        except sr.UnknownValueError:
            # speech not understood; ignore quietly to keep UI clean
            pass
        except sr.RequestError as e:
            msg_queue.put(f"[ERROR] API request failed: {e}")

    # Start background listening with short phrase chunks for responsiveness
    stop_func = r.listen_in_background(mic, callback, phrase_time_limit=3.2)

    print_header()

    try:
        # Drain messages and keep main thread alive
        while True:
            try:
                # Print any messages produced by callback
                line = msg_queue.get(timeout=0.2)
                print(line, flush=True)
            except queue.Empty:
                pass
            # You can do other work here if needed
    except KeyboardInterrupt:
        print("\nStopping...")
    finally:
        # Stop the background listener and give it a moment to exit cleanly
        stop_func(wait_for_stop=False)
        time.sleep(0.3)
        print("Goodbye!")


if __name__ == "__main__":
    main()