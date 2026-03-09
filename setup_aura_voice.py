import os
import sys
import platform
import subprocess
import urllib.request
import tarfile

def setup_piper():
    print("--- AURA // Piper TTS Auto-Setup ---")
    
    # 1. Detect Architecture
    arch = platform.machine().lower()
    print(f"[*] Detected Architecture: {arch}")
    
    if "aarch64" in arch:
        url = "https://github.com/rhasspy/piper/releases/download/v1.2.0/piper_linux_aarch64.tar.gz"
    elif "armv7" in arch:
        url = "https://github.com/rhasspy/piper/releases/download/v1.2.0/piper_linux_armv7l.tar.gz"
    elif "x86_64" in arch:
        url = "https://github.com/rhasspy/piper/releases/download/v1.2.0/piper_linux_x86_64.tar.gz"
    else:
        print(f"[!] Unsupported architecture '{arch}'. Please install Piper manually.")
        return

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

    # 3. Add to User Path (Simulated by telling user or creating a symlink)
    # For simplicity, we'll assume the binary is in the 'piper' folder created by extraction
    piper_path = os.path.abspath("piper/piper")
    if not os.path.exists(piper_path):
        # Handle different extraction folder names if necessary
        print("[!] Could not find piper binary in extracted folder.")
        return

    # 4. Download Voice Model (Amy Medium)
    model_name = "en_US-amy-medium.onnx"
    config_name = "en_US-amy-medium.onnx.json"
    model_url = f"https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/en/US/amy/medium/{model_name}"
    config_url = f"https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/en/US/amy/medium/{config_name}"

    print(f"[*] Downloading Voice Model: {model_name}")
    try:
        urllib.request.urlretrieve(model_url, model_name)
        urllib.request.urlretrieve(config_url, config_name)
        print("[+] Voice model and config downloaded.")
    except Exception as e:
        print(f"[!] Model download failed: {e}")
        return

    # 5. Create a system symlink or helper
    print("\n--- SETUP COMPLETE ---")
    print(f"[TIP] To make Piper available system-wide, run:")
    print(f"sudo ln -s {piper_path} /usr/local/bin/piper")
    print("\n[TEST] Verifying installation...")
    
    test_cmd = f'echo "Aura voice system is now online." | {piper_path} --model {model_name} --output_file test.wav'
    res = subprocess.run(test_cmd, shell=True)
    
    if res.returncode == 0:
        print("[SUCCESS] Piper generated test.wav successfully.")
        print("[ACTION] You can now run 'python app.py' to start Nikki with realistic voice.")
    else:
        print("[ERROR] Test generation failed. Check dependencies (libasound2, etc).")

if __name__ == "__main__":
    setup_piper()
