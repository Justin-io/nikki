python3 setup_aura_voice.py
sudo ln -s $(pwd)/piper/piper /usr/local/bin/piper
python3 app.py

(.venv) justin@hoperobot:~/Desktop/nikki $ python3 setup_aura_voice.py

==================================================
      AURA AI: BULLETPROOF VOCAL SETUP
==================================================
[*] Installing Premium Vocal Engine...
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
[*] Testing Player: /usr/bin/mpg123
[*] Executing Live Stream: edge-tts --voice en-US-AvaNeural --text "System online. Vocal core is now bulletproof." --write-media - | /usr/bin/mpg123 -Q -
mpg123: Unknown option "Q".
You made some mistake in program usage... let me briefly remind you:

High Performance MPEG 1.0/2.0/2.5 Audio Player for Layers 1, 2 and 3
	version 1.32.10; written and copyright by Michael Hipp and others
	free software (LGPL) without any warranty but with best wishes

usage: mpg123 [option(s)] [file(s) | URL(s) | -]
supported options [defaults in brackets]:
   -v    increase verbosity level       -q    quiet (don't print title)
   -t    testmode (no output)           -s    write to stdout
   -w f  write output as WAV file
   -k n  skip first n frames [0]        -n n  decode only n frames [all]
   -c    check range violations         -y    DISABLE resync on errors
   -b n  output buffer: n Kbytes [0]    -f n  change scalefactor [32768]
   -r n  set/force samplerate [auto]
   -o m  select output module           -a d  set audio device
   -2    downsample 1:2 (22 kHz)        -4    downsample 1:4 (11 kHz)
   -d n  play every n'th frame only     -h n  play every frame n times
   -0    decode channel 0 (left) only   -1    decode channel 1 (right) only
   -m    mix both channels (mono)       -p p  use HTTP proxy p [$HTTP_PROXY]
   -@ f  read filenames/URLs from f     -T get realtime priority
   -z    shuffle play (with wildcards)  -Z    random play
   -u a  HTTP authentication string     -E f  Equalizer, data from file
   -C    enable control keys            --no-gapless  not skip junk/padding in mp3s
   -?    this help                      --version  print name + version
See the manpage mpg123(1) or call mpg123 with --longhelp for more parameters and information.
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
client_session: <aiohttp.client.ClientSession object at 0x7f8eb2f4d0>
Task was destroyed but it is pending!
task: <Task pending name='Task-5' coro=<<async_generator_athrow without __name__>()> wait_for=<Future pending cb=[Task.task_wakeup()]>>

--- DONE ---
If you heard the voice, run: python3 app.py
