import os
import sys
import subprocess

def setup_aura_pro():
    print("\n" + "="*50)
    print("      AURA AI: BULLETPROOF VOCAL SETUP")
    print("="*50)
    
    # 1. Edge-TTS Install
    print("[*] Installing Premium Vocal Engine...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "edge-tts"])

    # 2. Test with Absolute Path (Bypasses shell errors)
    PLAYER = "/usr/bin/mpg123"
    print(f"[*] Testing Player: {PLAYER}")
    
    if not os.path.exists(PLAYER):
        print(f"[!] {PLAYER} NOT FOUND. Installing...")
        subprocess.run("sudo apt update && sudo apt install mpg123 -y", shell=True)

    test_text = "System online. Vocal core is now bulletproof."
    test_cmd = f'edge-tts --voice en-US-AvaNeural --text "{test_text}" --write-media - | {PLAYER} -Q -'
    
    print(f"[*] Executing Live Stream: {test_cmd}")
    subprocess.run(test_cmd, shell=True)
    
    print("\n--- DONE ---")
    print("If you heard the voice, run: python3 app.py")

if __name__ == "__main__":
    setup_aura_pro()
