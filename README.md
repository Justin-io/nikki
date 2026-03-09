atus HTTP/1.1" 200 -
^Z[4]   Killed                  python app.py

[5]+  Stopped                 python app.py
(.venv) justin@hoperobot:~/Desktop/nikki $ python3 setup_aura_voice.py
--- AURA // Vosk TTS Auto-Setup ---
[*] Installing vosk-tts...
Looking in indexes: https://pypi.org/simple, https://www.piwheels.org/simple
Collecting vosk-tts
  Downloading vosk_tts-0.3.61-py3-none-any.whl.metadata (1.4 kB)
Collecting onnxruntime>=1.14 (from vosk-tts)
  Downloading onnxruntime-1.24.3-cp313-cp313-manylinux_2_27_aarch64.manylinux_2_28_aarch64.whl.metadata (5.1 kB)
Requirement already satisfied: requests in /usr/lib/python3/dist-packages (from vosk-tts) (2.32.3)
Collecting tokenizers (from vosk-tts)
  Downloading tokenizers-0.22.2-cp39-abi3-manylinux_2_17_aarch64.manylinux2014_aarch64.whl.metadata (7.3 kB)
Requirement already satisfied: tqdm in /usr/lib/python3/dist-packages (from vosk-tts) (4.67.1)
Collecting flatbuffers (from onnxruntime>=1.14->vosk-tts)
  Downloading https://www.piwheels.org/simple/flatbuffers/flatbuffers-20181003210633-py2.py3-none-any.whl (14 kB)
Requirement already satisfied: numpy>=1.21.6 in /usr/lib/python3/dist-packages (from onnxruntime>=1.14->vosk-tts) (2.2.4)
Requirement already satisfied: packaging in /usr/lib/python3/dist-packages (from onnxruntime>=1.14->vosk-tts) (25.0)
Collecting protobuf (from onnxruntime>=1.14->vosk-tts)
  Downloading protobuf-7.34.0-cp310-abi3-manylinux2014_aarch64.whl.metadata (595 bytes)
Collecting sympy (from onnxruntime>=1.14->vosk-tts)
  Downloading https://www.piwheels.org/simple/sympy/sympy-1.14.0-py3-none-any.whl (6.3 MB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 6.3/6.3 MB 2.1 MB/s eta 0:00:00
Requirement already satisfied: charset_normalizer<4,>=2 in /usr/lib/python3/dist-packages (from requests->vosk-tts) (3.4.2)
Requirement already satisfied: idna<4,>=2.5 in /usr/lib/python3/dist-packages (from requests->vosk-tts) (3.10)
Requirement already satisfied: urllib3<3,>=1.21.1 in /usr/lib/python3/dist-packages (from requests->vosk-tts) (2.3.0)
Requirement already satisfied: certifi>=2017.4.17 in /usr/lib/python3/dist-packages (from requests->vosk-tts) (2025.1.31)
Collecting mpmath<1.4,>=1.1.0 (from sympy->onnxruntime>=1.14->vosk-tts)
  Downloading https://www.piwheels.org/simple/mpmath/mpmath-1.3.0-py3-none-any.whl (536 kB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 536.2/536.2 kB 966.5 kB/s eta 0:00:00
Collecting huggingface-hub<2.0,>=0.16.4 (from tokenizers->vosk-tts)
  Downloading https://www.piwheels.org/simple/huggingface-hub/huggingface_hub-1.6.0-py3-none-any.whl (612 kB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 612.9/612.9 kB 711.4 kB/s eta 0:00:00
Collecting filelock>=3.10.0 (from huggingface-hub<2.0,>=0.16.4->tokenizers->vosk-tts)
  Downloading https://www.piwheels.org/simple/filelock/filelock-3.25.0-py3-none-any.whl (26 kB)
Collecting fsspec>=2023.5.0 (from huggingface-hub<2.0,>=0.16.4->tokenizers->vosk-tts)
  Downloading https://www.piwheels.org/simple/fsspec/fsspec-2026.2.0-py3-none-any.whl (202 kB)
Collecting hf-xet<2.0.0,>=1.3.2 (from huggingface-hub<2.0,>=0.16.4->tokenizers->vosk-tts)
  Downloading hf_xet-1.3.2-cp37-abi3-manylinux_2_28_aarch64.whl.metadata (4.9 kB)
Collecting httpx<1,>=0.23.0 (from huggingface-hub<2.0,>=0.16.4->tokenizers->vosk-tts)
  Downloading https://www.piwheels.org/simple/httpx/httpx-0.28.1-py3-none-any.whl (73 kB)
Requirement already satisfied: pyyaml>=5.1 in /usr/lib/python3/dist-packages (from huggingface-hub<2.0,>=0.16.4->tokenizers->vosk-tts) (6.0.2)
Collecting typer (from huggingface-hub<2.0,>=0.16.4->tokenizers->vosk-tts)
  Downloading https://www.piwheels.org/simple/typer/typer-0.24.1-py3-none-any.whl (56 kB)
Requirement already satisfied: typing-extensions>=4.1.0 in /usr/lib/python3/dist-packages (from huggingface-hub<2.0,>=0.16.4->tokenizers->vosk-tts) (4.13.2)
Collecting anyio (from httpx<1,>=0.23.0->huggingface-hub<2.0,>=0.16.4->tokenizers->vosk-tts)
  Downloading https://www.piwheels.org/simple/anyio/anyio-4.12.1-py3-none-any.whl (113 kB)
Collecting httpcore==1.* (from httpx<1,>=0.23.0->huggingface-hub<2.0,>=0.16.4->tokenizers->vosk-tts)
  Downloading https://www.piwheels.org/simple/httpcore/httpcore-1.0.9-py3-none-any.whl (78 kB)
Collecting h11>=0.16 (from httpcore==1.*->httpx<1,>=0.23.0->huggingface-hub<2.0,>=0.16.4->tokenizers->vosk-tts)
  Downloading https://www.piwheels.org/simple/h11/h11-0.16.0-py3-none-any.whl (37 kB)
Collecting click>=8.2.1 (from typer->huggingface-hub<2.0,>=0.16.4->tokenizers->vosk-tts)
  Downloading https://www.piwheels.org/simple/click/click-8.3.1-py3-none-any.whl (108 kB)
Collecting shellingham>=1.3.0 (from typer->huggingface-hub<2.0,>=0.16.4->tokenizers->vosk-tts)
  Downloading https://www.piwheels.org/simple/shellingham/shellingham-1.5.4-py2.py3-none-any.whl (9.8 kB)
Requirement already satisfied: rich>=12.3.0 in /usr/lib/python3/dist-packages (from typer->huggingface-hub<2.0,>=0.16.4->tokenizers->vosk-tts) (13.9.4)
Collecting annotated-doc>=0.0.2 (from typer->huggingface-hub<2.0,>=0.16.4->tokenizers->vosk-tts)
  Downloading https://www.piwheels.org/simple/annotated-doc/annotated_doc-0.0.4-py3-none-any.whl (5.3 kB)
Requirement already satisfied: markdown-it-py>=2.2.0 in /usr/lib/python3/dist-packages (from rich>=12.3.0->typer->huggingface-hub<2.0,>=0.16.4->tokenizers->vosk-tts) (3.0.0)
Requirement already satisfied: pygments<3.0.0,>=2.13.0 in /usr/lib/python3/dist-packages (from rich>=12.3.0->typer->huggingface-hub<2.0,>=0.16.4->tokenizers->vosk-tts) (2.18.0)
Requirement already satisfied: mdurl~=0.1 in /usr/lib/python3/dist-packages (from markdown-it-py>=2.2.0->rich>=12.3.0->typer->huggingface-hub<2.0,>=0.16.4->tokenizers->vosk-tts) (0.1.2)
Downloading vosk_tts-0.3.61-py3-none-any.whl (12 kB)
Downloading onnxruntime-1.24.3-cp313-cp313-manylinux_2_27_aarch64.manylinux_2_28_aarch64.whl (15.1 MB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 15.1/15.1 MB 2.2 MB/s eta 0:00:00
Downloading protobuf-7.34.0-cp310-abi3-manylinux2014_aarch64.whl (325 kB)
Downloading tokenizers-0.22.2-cp39-abi3-manylinux_2_17_aarch64.manylinux2014_aarch64.whl (3.3 MB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 3.3/3.3 MB 1.5 MB/s eta 0:00:00
Downloading hf_xet-1.3.2-cp37-abi3-manylinux_2_28_aarch64.whl (4.0 MB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 4.0/4.0 MB 2.2 MB/s eta 0:00:00
Installing collected packages: mpmath, flatbuffers, sympy, shellingham, protobuf, hf-xet, h11, fsspec, filelock, click, anyio, annotated-doc, onnxruntime, httpcore, typer, httpx, huggingface-hub, tokenizers, vosk-tts
  Attempting uninstall: click
    Found existing installation: click 8.1.8
    Not uninstalling click at /usr/lib/python3/dist-packages, outside environment /home/justin/hope_attendance_system/.venv
    Can't uninstall 'click'. No files were found to uninstall.
ERROR: pip's dependency resolver does not currently take into account all the packages that are installed. This behaviour is the source of the following dependency conflicts.
types-flask-migrate 4.0 requires Flask-SQLAlchemy>=3.0.1, which is not installed.
Successfully installed annotated-doc-0.0.4 anyio-4.12.1 click-8.3.1 filelock-3.25.0 flatbuffers-20181003210633 fsspec-2026.2.0 h11-0.16.0 hf-xet-1.3.2 httpcore-1.0.9 httpx-0.28.1 huggingface-hub-1.6.0 mpmath-1.3.0 onnxruntime-1.24.3 protobuf-7.34.0 shellingham-1.5.4 sympy-1.14.0 tokenizers-0.22.2 typer-0.24.1 vosk-tts-0.3.61
[+] vosk-tts installed successfully.

--- MODEL SETUP ---
Vosk TTS requires a voice model. You can find them at:
https://alphacephei.com/vosk/models

Recommended for English:
Model: vosk-model-tts-en-us-0.10

[INSTRUCTION] Please download the model, extract it, and place it in the application folder.
Then update VOSK_TTS_MODEL in app.py to point to that directory.

[TEST] To verify installation manually, run:
vosk-tts --input "Aura voice system is now using Vosk." --output test_vosk.wav
aplay test_vosk.wav
(.venv) justin@hoperobot:~/Desktop/nikki $ vosk-tts --input "Aura voice system is now using Vosk." --output test_vosk.wav
aplay test_vosk.wav
2026-03-09 09:13:59.728391491 [W:onnxruntime:Default, device_discovery.cc:211 DiscoverDevicesForPlatform] GPU device discovery failed: device_discovery.cc:91 ReadFileContents Failed to open file: "/sys/class/drm/card1/device/vendor"
vosk-model-small-en-us-0.15.zip: 100%|██████| 39.3M/39.3M [01:26<00:00, 479kB/s]
INFO:root:Loading model from /home/justin/.cache/vosk/vosk-model-small-en-us-0.15
Traceback (most recent call last):
  File "/home/justin/hope_attendance_system/.venv/bin/vosk-tts", line 8, in <module>
    sys.exit(main())
             ~~~~^^
  File "/home/justin/hope_attendance_system/.venv/lib/python3.13/site-packages/vosk_tts/cli.py", line 63, in main
    model = Model(args.model, args.model_name, args.lang)
  File "/home/justin/hope_attendance_system/.venv/lib/python3.13/site-packages/vosk_tts/model.py", line 46, in __init__
    self.onnx = onnxruntime.InferenceSession(str(model_path / "model.onnx"), sess_options=sess_options, providers=providers)
                ~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/justin/hope_attendance_system/.venv/lib/python3.13/site-packages/onnxruntime/capi/onnxruntime_inference_collection.py", line 504, in __init__
    self._create_inference_session(providers, provider_options, disabled_optimizers)
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/justin/hope_attendance_system/.venv/lib/python3.13/site-packages/onnxruntime/capi/onnxruntime_inference_collection.py", line 599, in _create_inference_session
    sess = C.InferenceSession(session_options, self._model_path, True, self._read_config_from_model)
onnxruntime.capi.onnxruntime_pybind11_state.NoSuchFile: [ONNXRuntimeError] : 3 : NO_SUCHFILE : Load model from /home/justin/.cache/vosk/vosk-model-small-en-us-0.15/model.onnx failed:Load model /home/justin/.cache/vosk/vosk-model-small-en-us-0.15/model.onnx failed. File doesn't exist
test_vosk.wav: No such file or directory
(.venv) justin@hoperobot:~/Desktop/nikki $ 
