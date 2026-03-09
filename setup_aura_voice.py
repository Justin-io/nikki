import os
import sys
import subprocess

def setup_vosk_tts():
    print("--- AURA // Vosk TTS Auto-Setup ---")
    
    # 1. Install vosk-tts via pip
    print("[*] Installing vosk-tts...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "vosk-tts"])
        print("[+] vosk-tts installed successfully.")
    except Exception as e:
        print(f"[!] Failed to install vosk-tts: {e}")
        return

    # 2. Inform user about models
    print("\n--- MODEL SETUP ---")
    print("Vosk TTS requires a voice model. You can find them at:")
    print("https://alphacephei.com/vosk/models")
    print("\nRecommended for English:")
    print("Model: vosk-model-tts-en-us-0.10")
    print("\n[INSTRUCTION] Please download the model, extract it, and place it in the application folder.")
    print("Then update VOSK_TTS_MODEL in app.py to point to that directory.")

    # 3. Verification Command
    print("\n[TEST] To verify installation manually, run:")
    print('vosk-tts --input "Aura voice system is now using Vosk." --output test_vosk.wav')
    print("aplay test_vosk.wav")

if __name__ == "__main__":
    setup_vosk_tts()
