import os
import sys
import platform
import subprocess
import urllib.request
import tarfile
import time

def setup_aura_piper():
    print("\n" + "="*50)
    print("      AURA AI: LIVE TTS SETUP (PIPER)")
    print("="*50)
    
    # 1. Detect Architecture
    arch = platform.machine().lower()
    print(f"[*] Architecture: {arch}")
    
    # 2. Binary URLs
    if "aarch64" in arch:
        url = "https://github.com/rhasspy/piper/releases/download/2023.11.14-2/piper_linux_aarch64.tar.gz"
    elif "arm07" in arch or "armv7" in arch:
        url = "https://github.com/rhasspy/piper/releases/download/2023.11.14-2/piper_linux_armv7l.tar.gz"
    else:
        url = "https://github.com/rhasspy/piper/releases/download/2023.11.14-2/piper_linux_x86_64.tar.gz"

    # 3. Download & Extract
    if not os.path.exists("piper/piper"):
        print(f"[*] Downloading Piper engine...")
        try:
            urllib.request.urlretrieve(url, "piper.tar.gz")
            with tarfile.open("piper.tar.gz", "r:gz") as tar:
                tar.extractall()
            os.remove("piper.tar.gz")
            print("[+] Engine extracted.")
        except Exception as e:
            print(f"[!] Engine Download Error: {e}")
            return
    else:
        print("[*] Engine binary already present.")

    # 4. Voice Model
    model_name = "en_US-amy-medium.onnx"
    config_name = "en_US-amy-medium.onnx.json"
    if not os.path.exists(model_name):
        print("[*] Downloading Amy voice model (HuggingFace)...")
        m_url = f"https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/en/en_US/amy/medium/{model_name}"
        c_url = m_url + ".json"
        try:
            urllib.request.urlretrieve(m_url, model_name)
            urllib.request.urlretrieve(c_url, config_name)
            print("[+] Voice model ready.")
        except Exception as e:
            print(f"[!] Model Download Error: {e}")
            return
    else:
        print("[*] Voice model already present.")

    # 5. LIVE AUDIO TEST (The Real Deal)
    print("\n" + "-"*30)
    print("   LIVE AUDIO TEST (STREAMING)")
    print("-"*30)
    
    piper_path = os.path.abspath("piper/piper")
    model_path = os.path.abspath(model_name)
    
    # This command streams RAW audio directly to your speakers
    # No .wav file is created. It is real-time.
    test_cmd = (
        f'echo "Aura live audio test. If you hear this, real time speaking is working." | '
        f'"{piper_path}" --model "{model_path}" --output-raw | '
        f'aplay -r 22050 -f S16_LE -t raw'
    )
    
    print("[*] Running live pipe command...")
    print(f"Executing: {test_cmd}")
    
    try:
        # Run and check for errors
        res = subprocess.run(test_cmd, shell=True, capture_output=True, text=True)
        if res.returncode == 0:
            print("\n[SUCCESS] If you heard the voice, your Pi is 100% configured for real-time TTS.")
        else:
            print(f"\n[ERROR] Command failed with code {res.returncode}")
            print(f"Details: {res.stderr}")
            print("\n[TROUBLESHOOT] Try installing alsa utils: sudo apt install alsa-utils")
    except Exception as e:
        print(f"\n[CRITICAL ERROR] Failed to execute test: {e}")

    print("\n--- NEXT STEP ---")
    print("Run this to make it accessible to Nikki:")
    print(f"sudo ln -s {piper_path} /usr/local/bin/piper")
    print("\nThen start AURA: python3 app.py")

if __name__ == "__main__":
    setup_aura_piper()
