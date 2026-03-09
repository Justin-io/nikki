python3 setup_aura_voice.py
sudo ln -s $(pwd)/piper/piper /usr/local/bin/piper
python3 app.py


Then start AURA: python3 app.py
(.venv) justin@hoperobot:~/Desktop/nikki $ python3 setup_aura_voice.py

==================================================
      AURA AI: NEXT-GEN LIVE TTS (Edge-TTS)
==================================================
[*] Installing high-fidelity voice engine...
Looking in indexes: https://pypi.org/simple, https://www.piwheels.org/simple
Requirement already satisfied: edge-tts in /home/justin/hope_attendance_system/.venv/lib/python3.13/site-packages (7.2.7)
Requirement already satisfied: aiohttp<4.0.0,>=3.8.0 in /home/justin/hope_attendance_system/.venv/lib/python3.13/site-packages (from edge-tts) (3.13.3)
Requirement already satisfied: certifi>=2023.11.17 in /usr/lib/python3/dist-packages (from edge-tts) (2025.1.31)
Requirement already satisfied: tabulate<1.0.0,>=0.4.4 in /home/justin/hope_attendance_system/.venv/lib/python3.13/site-packages (from edge-tts) (0.9.0)
Requirement already satisfied: typing-extensions<5.0.0,>=4.1.0 in /usr/lib/python3/dist-packages (from edge-tts) (4.13.2)
Requirement already satisfied: aiohappyeyeballs>=2.5.0 in /home/justin/hope_attendance_system/.venv/lib/python3.13/site-packages (from aiohttp<4.0.0,>=3.8.0->edge-tts) (2.6.1)
Requirement already satisfied: aiosignal>=1.4.0 in /home/justin/hope_attendance_system/.venv/lib/python3.13/site-packages (from aiohttp<4.0.0,>=3.8.0->edge-tts) (1.4.0)
Requirement already satisfied: attrs>=17.3.0 in /usr/lib/python3/dist-packages (from aiohttp<4.0.0,>=3.8.0->edge-tts) (25.3.0)
Requirement already satisfied: frozenlist>=1.1.1 in /home/justin/hope_attendance_system/.venv/lib/python3.13/site-packages (from aiohttp<4.0.0,>=3.8.0->edge-tts) (1.8.0)
Requirement already satisfied: multidict<7.0,>=4.5 in /home/justin/hope_attendance_system/.venv/lib/python3.13/site-packages (from aiohttp<4.0.0,>=3.8.0->edge-tts) (6.7.1)
Requirement already satisfied: propcache>=0.2.0 in /home/justin/hope_attendance_system/.venv/lib/python3.13/site-packages (from aiohttp<4.0.0,>=3.8.0->edge-tts) (0.4.1)
Requirement already satisfied: yarl<2.0,>=1.17.0 in /home/justin/hope_attendance_system/.venv/lib/python3.13/site-packages (from aiohttp<4.0.0,>=3.8.0->edge-tts) (1.22.0)
Requirement already satisfied: idna>=2.0 in /usr/lib/python3/dist-packages (from yarl<2.0,>=1.17.0->aiohttp<4.0.0,>=3.8.0->edge-tts) (3.10)
[+] Engine installed.
[*] Checking audio hardware...
[*] Executing live test: edge-tts --voice en-US-AvaNeural --text "Aura core initialized. Live vocal system is now online." --write-media - | mpv -
/bin/sh: 1: mpv: not found
Traceback (most recent call last):
  File "/home/justin/hope_attendance_system/.venv/bin/edge-tts", line 8, in <module>
    sys.exit(main())
             ~~~~^^
  File "/home/justin/hope_attendance_system/.venv/lib/python3.13/site-packages/edge_tts/util.py", line 141, in main
    asyncio.run(amain())
    ~~~~~~~~~~~^^^^^^^^^
  File "/usr/lib/python3.13/asyncio/runners.py", line 195, in run
    return runner.run(main)
           ~~~~~~~~~~^^^^^^
  File "/usr/lib/python3.13/asyncio/runners.py", line 118, in run
    return self._loop.run_until_complete(task)
           ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^
  File "/usr/lib/python3.13/asyncio/base_events.py", line 725, in run_until_complete
    return future.result()
           ~~~~~~~~~~~~~^^
  File "/home/justin/hope_attendance_system/.venv/lib/python3.13/site-packages/edge_tts/util.py", line 136, in amain
    await _run_tts(args)
  File "/home/justin/hope_attendance_system/.venv/lib/python3.13/site-packages/edge_tts/util.py", line 75, in _run_tts
    audio_file.write(chunk["data"])
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^
BrokenPipeError: [Errno 32] Broken pipe
Exception ignored on flushing sys.stdout:
BrokenPipeError: [Errno 32] Broken pipe
Unclosed client session
client_session: <aiohttp.client.ClientSession object at 0x7faefdf4d0>
Task was destroyed but it is pending!
task: <Task pending name='Task-5' coro=<<async_generator_athrow without __name__>()> wait_for=<Future pending cb=[Task.task_wakeup()]>>

--- SETUP COMPLETE ---
AURA is now configured for ultra-realistic human speech.
Run Nikki: python3 app.py
(.venv) justin@hoperobot:~/Desktop/nikki $ 
