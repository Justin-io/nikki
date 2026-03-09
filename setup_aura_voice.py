import os
import sys
import subprocess
import time

def check_player():
    for player in ["mpg123", "mpv", "play", "aplay"]:
        if subprocess.run(f"command -v {player}", shell=True, capture_output=True).returncode == 0:
            return player
    return None

def setup_aura_vocal():
    print("\n" + "="*50)
    print("      AURA AI: MULTI-ENGINE VOCAL SETUP")
    print("="*50)
    
    # 1. Install edge-tts (Premium Cloud Engine)
    print("[*] Installing Edge-TTS...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "edge-tts"])
    except: pass

    # 2. Find a Player
    player = check_player()
    if not player:
        print("[!] NO AUDIO PLAYER FOUND. Please install one:")
        print("sudo apt update && sudo apt install mpg123 aplay mpv -y")
        return

    print(f"[*] Using Audio Player: {player}")

    # 3. LIVE TEST (Edge-TTS)
    print("\n" + "-"*30)
    print("   LIVE STREAM TEST")
    print("-"*30)
    
    test_text = "Aura vocal system test. If you hear this, everything is working perfectly."
    
    # Construct streaming command based on player
    if player == "mpg123":
        cmd = f'edge-tts --voice en-US-AvaNeural --text "{test_text}" --write-media - | mpg123 -Q -'
    elif player == "mpv":
        cmd = f'edge-tts --voice en-US-AvaNeural --text "{test_text}" --write-media - | mpv --no-terminal -'
    else:
        # Fallback to local file test if direct pipe is tricky
        cmd = f'edge-tts --voice en-US-AvaNeural --text "{test_text}" --write-media test.mp3 && {player} test.mp3'

    print(f"[*] Executing: {cmd}")
    subprocess.run(cmd, shell=True)
    
    print("\n--- NEXT STEP ---")
    print("If you heard the voice, run: python3 app.py")
    print("If you heard NOTHING, check your volume or run 'aplay -l' to check cards.")

if __name__ == "__main__":
    setup_aura_vocal()
