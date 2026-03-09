import os
import sys
import subprocess

def setup_aura_edge_tts():
    print("\n" + "="*50)
    print("      AURA AI: NEXT-GEN LIVE TTS (Edge-TTS)")
    print("="*50)
    
    # 1. Install edge-tts
    print("[*] Installing high-fidelity voice engine...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "edge-tts"])
        print("[+] Engine installed.")
    except Exception as e:
        print(f"[!] Installation failed: {e}")
        return

    # 2. Verify Audio Output
    print("[*] Checking audio hardware...")
    try:
        # Test with mpv (which we confirmed is on the system)
        test_txt = "Aura core initialized. Live vocal system is now online."
        # Use a high-quality human voice: en-US-AvaNeural
        test_cmd = f'edge-tts --voice en-US-AvaNeural --text "{test_txt}" --write-media - | mpv -'
        print(f"[*] Executing live test: {test_cmd}")
        subprocess.run(test_cmd, shell=True)
    except Exception as e:
        print(f"[!] Test failed: {e}")

    print("\n--- SETUP COMPLETE ---")
    print("AURA is now configured for ultra-realistic human speech.")
    print("Run Nikki: python3 app.py")

if __name__ == "__main__":
    setup_aura_edge_tts()
