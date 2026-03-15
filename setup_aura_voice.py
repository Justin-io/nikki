import os
import sys
import subprocess

def setup_aura_pro():
    print("\n" + "="*50)
    print("      AURA AI: BULLETPROOF VOCAL SETUP")
    print("="*50)
    
    # 1. Edge-TTS Install
    print("[*] Installing Premium Vocal Engine...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "edge-tts", "--break-system-packages"])

    # 2. Test with Absolute Path (Bypasses shell errors)
    PLAYER = "/usr/bin/mpg123"
    print(f"[*] Testing Player: {PLAYER}")
    
    if not os.path.exists(PLAYER):
        print(f"[!] {PLAYER} NOT FOUND. Installing...")
        subprocess.run("sudo apt update && sudo apt install mpg123 -y", shell=True)

    test_text = "System online. Vocal core is now bulletproof."
    print(f"[*] Executing Live Stream test.")
    
    p1 = subprocess.Popen([sys.executable, "-m", "edge_tts", "--voice", "en-US-AvaNeural", "--text", test_text, "--write-media", "-"], stdout=subprocess.PIPE)
    # Using buffer prevents choppiness on Pi 4
    p2 = subprocess.Popen([PLAYER, "-q", "--buffer", "1024", "-"], stdin=p1.stdout)
    p1.stdout.close()
    p2.communicate()
    
    print("\n--- DONE ---")
    print("If you heard the voice, run: python3 app.py")

if __name__ == "__main__":
    setup_aura_pro()
