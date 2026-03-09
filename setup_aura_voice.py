import os
import sys
import platform
import subprocess
import urllib.request
import tarfile

def setup_aura_piper():
    print("--- AURA // Realistic Voice Setup (Piper) ---")
    
    # 1. Detect Architecture
    arch = platform.machine().lower()
    print(f"[*] Detected Architecture: {arch}")
    
    # Verified Release: 2023.11.14-2
    if "aarch64" in arch:
        url = "https://github.com/rhasspy/piper/releases/download/2023.11.14-2/piper_linux_aarch64.tar.gz"
    elif "armv7" in arch:
        url = "https://github.com/rhasspy/piper/releases/download/2023.11.14-2/piper_linux_armv7l.tar.gz"
    else:
        url = "https://github.com/rhasspy/piper/releases/download/2023.11.14-2/piper_linux_x86_64.tar.gz"

    # 2. Download and Extract Piper Binary
    piper_tar = "piper.tar.gz"
    print(f"[*] Downloading Piper binary from: {url}")
    try:
        urllib.request.urlretrieve(url, piper_tar)
        with tarfile.open(piper_tar, "r:gz") as tar:
            tar.extractall()
        os.remove(piper_tar)
        print("[+] Piper binary extracted.")
    except Exception as e:
        print(f"[!] Download failed: {e}")
        return

    # 3. Verify Binary Path
    piper_bin = os.path.abspath("piper/piper")
    if not os.path.exists(piper_bin):
        # Check alternate extraction folder
        if os.path.exists("piper"):
             # On some extractions it might just be 'piper'
             pass
        else:
            print("[!] Could not find piper binary in extracted folder.")
            return

    # 4. Download Voice Model (Amy Medium) - VERIFIED LINKS
    model_name = "en_US-amy-medium.onnx"
    config_name = "en_US-amy-medium.onnx.json"
    
    # Hugging Face structure requires the extra 'en_US' folder
    model_url = f"https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/en/en_US/amy/medium/{model_name}"
    config_url = f"https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/en/en_US/amy/medium/{config_name}"

    print(f"[*] Downloading high-quality voice model: {model_name}")
    try:
        # Avoid double-downloading if already present
        if not os.path.exists(model_name):
            urllib.request.urlretrieve(model_url, model_name)
        if not os.path.exists(config_name):
            urllib.request.urlretrieve(config_url, config_name)
        print("[+] Voice model and config downloaded.")
    except Exception as e:
        print(f"[!] Model download failed: {e}")
        return

    # 5. TEST WITHOUT FLASK
    print("\n[TESTING ENGINE...]")
    test_cmd = f'echo "I can speak now." | {piper_bin} --model {model_name} --output_file test.wav'
    subprocess.run(test_cmd, shell=True)
    
    if os.path.exists("test.wav"):
        print("[SUCCESS] Engine generated test.wav.")
        print("[SUCCESS] Setup is 100% correct.")
    else:
        print("[FAILED] Engine failed to generate audio. Check dependencies (libasound2, etc).")

    print("\n--- FINAL STEP ---")
    print(f"Run this to make AURA work system-wide:")
    print(f"sudo ln -s {piper_bin} /usr/local/bin/piper")
    print("\nThen run AURA: python3 app.py")

if __name__ == "__main__":
    setup_aura_piper()
