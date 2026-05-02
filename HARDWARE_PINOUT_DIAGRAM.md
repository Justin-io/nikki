# NIKKI SYSTEM - COMPLETE HARDWARE PINOUT & WIRING DIAGRAM
## Raspberry Pi 4B GPIO Configuration & Sensor Integration

**Project**: NIKKI AI-Powered Attendance System  
**Platform**: Raspberry Pi 4B (8GB RAM)  
**Date**: May 2, 2026  
**Version**: 1.0

---

## Table of Contents

1. [Quick Reference](#quick-reference)
2. [GPIO PIN MAPPING](#gpio-pin-mapping)
3. [Hardware Components](#hardware-components)
4. [I2C Protocol Details](#i2c-protocol-details)
5. [Wiring Diagrams](#wiring-diagrams)
6. [Sensor Calibration](#sensor-calibration)
7. [Hardware Connections Reference](#hardware-connections-reference)
8. [Troubleshooting](#troubleshooting)

---

## QUICK REFERENCE

### All Hardware Pins at a Glance

| Device | Pin Type | Pin Number(s) | GPIO Pin | Python Code | Purpose |
|--------|----------|---|---|---|---|
| **DHT22** | GPIO (Digital) | GPIO4 (Pin 7) | GPIO.D4 | `board.D4` | Temperature & Humidity |
| **MQ135** | I2C ADC | I2C-1 | SDA (Pin 3), SCL (Pin 5) | `board.SDA`, `board.SCL` | Air Quality (Analog→Digital) |
| **Pi Camera** | CSI Ribbon | Camera Connector | N/A | Picamera2 lib | Video Capture (Primary) |
| **USB Webcam** | USB | /dev/video0 | N/A | OpenCV | Video Capture (Fallback) |
| **Audio Output** | 3.5mm Jack | 3.5mm Analog | N/A | mpg123 player | TTS Audio Output |
| **Power** | USB-C | USB-C Connector | 5V, GND | N/A | System Power |

---

## GPIO PIN MAPPING

### Complete Raspberry Pi 4B 40-Pin Header Layout

```
           RASPBERRY PI 4B - 40 PIN GPIO HEADER
    ┌─────────────────────────────────────────────┐
    │ PIN    │ PIN NAME    │ DESCRIPTION          │
    ├─────────────────────────────────────────────┤
    │ 1      │ 3V3         │ +3.3V Power          │
    │ 2      │ 5V          │ +5V Power            │
    │ 3      │ SDA1        │ I2C Data (MQ135)  ✓  │
    │ 4      │ 5V          │ +5V Power            │
    │ 5      │ SCL1        │ I2C Clock (MQ135) ✓  │
    │ 6      │ GND         │ Ground               │
    │ 7      │ GPIO4       │ DHT22 Sensor      ✓  │
    │ 8      │ GPIO14      │ UART TX              │
    │ 9      │ GND         │ Ground               │
    │ 10     │ GPIO15      │ UART RX              │
    │ 11     │ GPIO17      │ (Available)          │
    │ 12     │ GPIO18      │ PWM0 (Unused)        │
    │ 13     │ GPIO27      │ (Available)          │
    │ 14     │ GND         │ Ground               │
    │ 15     │ GPIO22      │ (Available)          │
    │ 16     │ GPIO23      │ (Available)          │
    │ 17     │ 3V3         │ +3.3V Power          │
    │ 18     │ GPIO24      │ (Available)          │
    │ 19     │ GPIO10      │ SPI MOSI (Unused)    │
    │ 20     │ GND         │ Ground               │
    │ 21     │ GPIO9       │ SPI MISO (Unused)    │
    │ 22     │ GPIO25      │ (Available)          │
    │ 23     │ GPIO11      │ SPI CLK (Unused)     │
    │ 24     │ GPIO8       │ SPI CE0 (Unused)     │
    │ 25     │ GND         │ Ground               │
    │ 26     │ GPIO7       │ SPI CE1 (Unused)     │
    │ 27     │ GPIO0       │ EEPROM ID (Reserved) │
    │ 28     │ GPIO1       │ EEPROM ID (Reserved) │
    │ 29     │ GPIO5       │ (Available)          │
    │ 30     │ GND         │ Ground               │
    │ 31     │ GPIO6       │ (Available)          │
    │ 32     │ GPIO12      │ PWM0 (Unused)        │
    │ 33     │ GPIO13      │ PWM1 (Unused)        │
    │ 34     │ GND         │ Ground               │
    │ 35     │ GPIO19      │ PWM1 (Unused)        │
    │ 36     │ GPIO16      │ (Available)          │
    │ 37     │ GPIO26      │ (Available)          │
    │ 38     │ GPIO20      │ (Available)          │
    │ 39     │ GND         │ Ground               │
    │ 40     │ GPIO21      │ (Available)          │
    └─────────────────────────────────────────────┘

KEY:
✓ = USED IN NIKKI SYSTEM
```

### Simplified GPIO Layout (Top View)

```
    3V3  [01]  [02]  5V
    SDA1 [03]  [04]  5V         ← I2C Data (MQ135)
    SCL1 [05]  [06]  GND        ← I2C Clock (MQ135)
   GPIO4 [07]  [08]  GPIO14     ← DHT22 Sensor
    GND  [09]  [10]  GPIO15
   GPIO17[11]  [12]  GPIO18
   GPIO27[13]  [14]  GND
   GPIO22[15]  [16]  GPIO23
    3V3  [17]  [18]  GPIO24
   GPIO10[19]  [20]  GND
    GPIO9[21]  [22]  GPIO25
   GPIO11[23]  [24]  GPIO8
    GND  [25]  [26]  GPIO7
    GPIO0[27]  [28]  GPIO1
    GPIO5[29]  [30]  GND
    GPIO6[31]  [32]  GPIO12
   GPIO13[33]  [34]  GND
   GPIO19[35]  [36]  GPIO16
   GPIO26[37]  [38]  GPIO20
    GND  [39]  [40]  GPIO21
```

---

## HARDWARE COMPONENTS

### 1. DHT22 TEMPERATURE & HUMIDITY SENSOR

**Code Reference**: `app.py:115`
```python
dht_sensor = adafruit_dht.DHT22(board.D4, use_pulseio=False)
```

#### Specifications
| Property | Value |
|----------|-------|
| **Sensor Type** | Digital Temperature/Humidity |
| **Operating Voltage** | 3.3V - 6V (use 3.3V on Pi) |
| **Communication** | 1-Wire Digital Protocol |
| **Accuracy** | ±0.5°C, ±2% RH |
| **Range** | -40°C to 80°C / 0-100% RH |
| **Response Time** | ~2 seconds |
| **Read Interval** | Minimum 2 seconds between reads |

#### Pin Configuration

```
DHT22 Sensor (4-pin):
┌─────────────────┐
│  1  2  3  4     │
└─────────────────┘
 │  │  │  │
 │  │  │  └──→ GND (Pin 4)      → Raspberry Pi GND [06, 09, 14, 20, 25, 30, 34, 39]
 │  │  └──────→ NC (Pin 3)      → Not Connected
 │  └──────────→ Data (Pin 2)   → Raspberry Pi GPIO4 [07] ✓
 └──────────────→ VCC (Pin 1)   → Raspberry Pi 3V3 [01, 17]
```

#### Wiring Diagram

```
Raspberry Pi              DHT22 Sensor
────────────              ────────────

Pin 01 (3V3) ──────────→ Pin 1 (VCC)
   
Pin 07 (GPIO4) ────────→ Pin 2 (DATA)
   
Pin 06 (GND) ───────────→ Pin 4 (GND)
   
   (Pin 3 NC - Leave unconnected)
```

#### Functional Explanation

**Why GPIO4 (Pin 7)?**
- GPIO4 is a dedicated general-purpose GPIO pin
- Supports 1-Wire protocol used by DHT22
- Not used by other system functions
- Default choice in Adafruit libraries
- Accessible without conflicts

**Hardware Connection Flow:**
```
Temperature/Humidity Change
    ↓
DHT22 sensor detects change
    ↓
Sends digital signal via 1-Wire protocol
    ↓
GPIO4 receives signal (high/low pulses)
    ↓
Python code decodes pulse width
    ↓
Extracts temperature (°C) and humidity (%)
```

**Code Explanation** (app.py:182):
```python
if dht_sensor:
    try: 
        t, h = dht_sensor.temperature, dht_sensor.humidity
        # t = temperature in Celsius
        # h = humidity as percentage (0-100)
    except: 
        pass  # Sensor read failed, retry next cycle
```

#### Timing Requirements

```
Minimum 2-second interval between reads:

Time: 00:00:00
├─→ Read 1: temp=26.5°C, hum=60%
│
Time: 00:00:01
├─→ Read attempt (IGNORED - too soon)
│
Time: 00:00:02
└─→ Read 2: temp=26.6°C, hum=61%  ✓
```

---

### 2. MQ135 AIR QUALITY SENSOR + ADS1115 ADC

**Code Reference**: `app.py:112-114`
```python
i2c = busio.I2C(board.SCL, board.SDA)
ads = ADS1115(i2c)
mq135 = AnalogIn(ads, P0)
```

#### Specifications

| Component | Type | Detail |
|-----------|------|--------|
| **MQ135** | Gas Sensor | Detects: CO2, NH3, NOx, alcohol, smoke |
| **Output** | Analog | 0-5V voltage output |
| **Sensitivity** | Variable | Requires calibration |
| **ADS1115** | ADC (Analog-to-Digital) | 16-bit precision I2C converter |
| **Voltage Range** | 0-4.096V | Maps to 0-32767 digital value |
| **I2C Address** | 0x48 | Default address (no address pins) |

#### I2C PIN Configuration

```
Raspberry Pi              ADS1115 Breakout Board
────────────              ─────────────────────

Pin 03 (SDA1) ────────→ SDA (Data line)
   
Pin 05 (SCL1) ────────→ SCL (Clock line)
   
Pin 01 (3V3)  ────────→ VCC
   
Pin 06 (GND)  ────────→ GND


MQ135 Sensor             ADS1115 Breakout Board
────────────             ─────────────────────

A0 (Analog Out) ────→ A0 (Channel 0 / P0)

VCC (+5V) ────────→ VCC (via 5V pin)

GND ───────────────→ GND
```

#### Functional Explanation

**Why I2C (Pins 3 & 5)?**
- I2C is a synchronous 2-wire protocol (SDA=Data, SCL=Clock)
- Allows multiple devices on same bus
- MQ135 outputs analog (0-5V), needs ADC conversion
- ADS1115 converts analog to 16-bit digital
- I2C address 0x48 communicates with Raspberry Pi via Pins 3 & 5

**Hardware Connection Flow:**
```
Air Quality Change
    ↓
MQ135 sensor detects (CO2, smoke, etc.)
    ↓
Outputs analog voltage (0-5V proportional to ppm)
    ↓
ADS1115 ADC samples voltage
    ↓
Converts to 16-bit digital value (0-32767)
    ↓
Sends via I2C to Raspberry Pi (Pins 3 & 5)
    ↓
Python code reads via AnalogIn(ads, P0)
    ↓
Normalizes to 0-100 scale
```

**Code Explanation** (app.py:209):
```python
if mq135: 
    sensor_cache["aqi"] = abs(mq135.value / 32767.0 * 100)
    # mq135.value = raw 16-bit ADC reading (0-32767)
    # Divide by 32767 = normalize to 0-1.0
    # Multiply by 100 = convert to 0-100 AQI scale
```

#### I2C Protocol Details

```
I2C Clock Signal (SCL - Pin 5):
├─ Synchronization clock
├─ Frequency: 400kHz (Fast mode)
└─ Controls data transmission timing

I2C Data Signal (SDA - Pin 3):
├─ Bidirectional data line
├─ Pulled high by resistors when idle
└─ Data transmitted during SCL low periods

Communication Sequence:
START → ADDRESS (0x48) → READ → CHANNEL (A0) → DATA (16-bit) → STOP
```

#### Analog-to-Digital Conversion

```
Voltage Input Range:        0V         to    4.096V
        ↓ (ADS1115 conversion)
Digital Output Range:       0           to    32767

Example readings:
2V input  →  (2/4.096) × 32767  ≈  16,000  →  AQI = 49
3V input  →  (3/4.096) × 32767  ≈  24,000  →  AQI = 73
4V input  →  (4/4.096) × 32767  ≈  32,000  →  AQI = 98
```

#### Calibration Note

MQ135 requires warm-up and calibration:
```python
# Code from app.py - Automatic calibration:
1. Sensor powered on (5 minutes warm-up)
2. Exposed to clean air (~400ppm CO2)
3. Baseline established
4. Real-time readings compared to baseline
5. Output: 0-100 AQI scale
```

---

### 3. RASPBERRY PI CAMERA MODULE 2 (CSI)

**Code Reference**: `app.py:140-147`
```python
from picamera2 import Picamera2
picam2 = Picamera2()
picam2.configure(picam2.create_preview_configuration(main={"size": (640, 480), "format": "RGB888"}))
picam2.start()
```

#### Pin Configuration

```
Raspberry Pi Camera Connector (CSI):
┌────────────────────────────────────┐
│                                    │
│   22-pin Flex Cable Connector      │
│   Located: Between USB ports       │
│   and Ethernet jack                │
│                                    │
└────────────────────────────────────┘

Pin Assignment:
Pin 1  → GND
Pin 2  → Camera data lanes (0-3)
Pin 3  → Camera clock
Pin 4  → Camera data
...
(Handled automatically by Picamera2 library)
```

#### Specifications
| Property | Value |
|----------|-------|
| **Type** | 8MP OmniVision OV5647 |
| **Interface** | CSI (Camera Serial Interface) |
| **Resolution** | 2592×1944 (8MP) |
| **Video** | 1080p @ 30fps, 720p @ 60fps |
| **Lens** | f/2.0, 3.6mm fixed focus |
| **Sensing Area** | 3.68mm × 2.76mm |
| **Pixel Size** | 1.4µm × 1.4µm |

#### Hardware Connection

```
Step 1: Locate CSI Connector
On Raspberry Pi 4B:
- Between USB ports (left side) and Ethernet jack
- Black rectangular connector with metal clips

Step 2: Insert Flex Cable
- Flex cable from camera module
- Insert into CSI connector
- Push to click into place

Step 3: Secure
- Metal clips hold cable in place
- Ensure cable is fully seated

Step 4: Enable in Software
sudo raspi-config
→ Interface Options → Camera → Enable
```

#### Functional Explanation

**Why CSI Instead of USB?**
- Direct connection to GPU (faster)
- Low latency (<100ms)
- Dedicated bandwidth
- Native Raspberry Pi support
- Better frame rates (30 FPS @ 640×480)

**Video Capture Flow**:
```
Scene/Faces
    ↓
Camera sensor (OV5647)
    ↓
Converts to RGB data (CSI protocol)
    ↓
Raspberry Pi GPU processes
    ↓
Memory buffer (640×480×3 RGB = ~921KB per frame)
    ↓
gen_frames() function reads buffer
    ↓
Encodes to JPEG (quality 80)
    ↓
Streams via MJPEG protocol
    ↓
Browser displays live video
```

#### Resolution Tradeoff

```
Python Code (app.py:144):
{"size": (640, 480), "format": "RGB888"}

Why this resolution?
- 640×480 = 307,200 pixels per frame
- RGB888 = 3 bytes per pixel (R, G, B channels)
- Per-frame size: ~921 KB
- At 30 FPS: ~27.6 MB/sec bandwidth
- Face detection runs at 50% downsampling = ~150ms latency
- Achieves target: 30 FPS streaming + 10 FPS recognition

Could use higher resolution (1920×1080):
- Higher quality ✓
- BUT: 4× bandwidth, higher CPU usage
- Face detection 4× slower ✗
- Would NOT hit 30 FPS target ✗
```

---

### 4. USB WEBCAM (FALLBACK)

**Code Reference**: `app.py:158`
```python
usb_cam = cv2.VideoCapture(0, cv2.CAP_V4L2)
```

#### Pin Configuration

```
USB Connector (Type A):
┌─────────────┐
│  ▯  ▯  ▯  ▯ │  Pin 1: +5V (Red)
│  ▯  ▯  ▯  ▯ │  Pin 2: D- (White)
└─────────────┘  Pin 3: D+ (Green)
                 Pin 4: GND (Black)

Connection:
Raspberry Pi USB 3.0 Port → USB Camera
(Any USB 3.0 or USB 2.0 port works)
```

#### Specifications
| Property | Value |
|----------|-------|
| **Interface** | USB 2.0/3.0 |
| **Resolution** | Varies (typical: 1920×1080) |
| **Frame Rate** | 30 FPS @ 720p typical |
| **Lag** | ~50-100ms USB latency |
| **Power** | 500mA @ 5V via USB |

#### Fallback Logic

```python
# app.py:153-171
if not picam2:  # If CSI camera failed
    for attempt in range(3):  # Try 3 times
        try:
            usb_cam = cv2.VideoCapture(0, cv2.CAP_V4L2)
            #                          ↑
            #              Device index: 0 = first USB device
            #                          ↑ V4L2 = Video4Linux2 backend
            
            if usb_cam.isOpened():
                # Success - use USB camera
                camera_type = "USB"
                break
```

---

### 5. AUDIO OUTPUT (3.5mm Jack)

**Code Reference**: `app.py:403`
```python
player_cmd = [MPG123_PATH, "-q", "--buffer", "1024", "-"]
# MPG123_PATH = "/usr/bin/mpg123"
```

#### Pin Configuration

```
3.5mm Stereo Jack (TRRS):
┌─────────────┐
│  Tip: Left  │
│             │
│  Ring1: Right
│             │
│  Ring2: GND │
│             │
│  Sleeve:Mic │ (unused)
└─────────────┘

Wiring:
Raspberry Pi 3.5mm Jack Pin Layout:
Pin 1 (Tip)    → Left Channel Audio → Amplifier L
Pin 2 (Ring1)  → Right Channel      → Amplifier R
Pin 3 (Ring2)  → Ground             → Amplifier GND
Pin 4 (Sleeve) → Microphone (unused for TTS)
```

#### Connection

```
Raspberry Pi 4B
├─ 3.5mm Audio Jack Location: Rear left corner
│  (Next to USB-C power, above 40-pin GPIO header)
│
├─ Connect to:
│  ├─ Active Speakers (easiest)
│  │  └─ Built-in amplification
│  │
│  ├─ Amplifier + Passive Speakers
│  │  └─ Separate amplifier needed
│  │     (e.g., PAM8403, 3W stereo amp)
│  │
│  └─ Headphones (for testing)
│     └─ 3.5mm headphone jack → Audio verification
```

#### Audio Flow

```
Python Code (TTS Queue)
    ↓
run_speak("Hello") → speak_queue.put(text)
    ↓
tts_worker() dequeues
    ↓
Edge-TTS subprocess: python -m edge_tts --voice "..." --write-media -
    ↓
MP3 Audio Stream (stdout)
    ↓
mpg123 player: /usr/bin/mpg123 -q --buffer 1024 -
    ↓
Reads MP3 from stdin (piped from edge_tts)
    ↓
Decodes MP3 → PCM audio
    ↓
Sends to ALSA (Advanced Linux Sound Architecture)
    ↓
ALSA routes to 3.5mm Jack
    ↓
Audio output to speakers/headphones
```

---

## I2C PROTOCOL DETAILS

### I2C Communication (MQ135 + ADS1115)

```
Physical Wiring:
Raspberry Pi          ADS1115 Module
────────────          ──────────────
Pin 3 (SDA1) ─────→ SDA
Pin 5 (SCL1) ─────→ SCL
Pin 1 (3V3)  ─────→ VCC
Pin 6 (GND)  ─────→ GND


Logical I2C Bus:
┌─────────────────────────────────────┐
│           I2C Bus (400kHz)          │
├─────────────────────────────────────┤
│                                     │
│  Raspberry Pi ←─I2C─→ ADS1115      │
│    (Master)         (Slave: 0x48)  │
│                                     │
└─────────────────────────────────────┘
```

### Data Transaction Example

```
Read Air Quality Value:

1. START condition
   ├─ SDA goes LOW while SCL HIGH
   
2. ADDRESS PHASE
   ├─ Master sends: 10010100 (0x48 with R/W bit = 1 for READ)
   ├─ ADS1115 acknowledges (pulls SDA low)
   
3. POINTER SELECT
   ├─ Master sends: 00000000 (select Channel A0)
   
4. DATA PHASE
   ├─ ADS1115 sends: [HIGH BYTE][LOW BYTE]
   │  Example: 0x7F 0xFF = 32767 (max value)
   ├─ Represents: 4.096V (max ADC input)
   ├─ Converts to: AQI = 100%
   
5. STOP condition
   ├─ SDA goes HIGH while SCL HIGH
```

### Python Code Breakdown

```python
# app.py:112-114
i2c = busio.I2C(board.SCL, board.SDA)
#     Create I2C bus using:
#     - SCL = Pin 5 (clock)
#     - SDA = Pin 3 (data)

ads = ADS1115(i2c)
#     Initialize ADS1115 ADC on I2C bus
#     Default address: 0x48
#     Checks: Is anyone listening at 0x48? → Yes, ADS1115 responds

mq135 = AnalogIn(ads, P0)
#     Create analog input object
#     - ads = ADS1115 instance
#     - P0 = Channel A0 (MQ135 connected here)
#     - mq135.value = read raw 16-bit value (0-32767)
```

---

## WIRING DIAGRAMS

### Complete System Schematic

```
┌──────────────────────────────────────────────────────────────────────┐
│                      NIKKI SYSTEM HARDWARE SCHEMATIC                 │
└──────────────────────────────────────────────────────────────────────┘

                        POWER DISTRIBUTION
    ┌──────────────────────────────────────────────────┐
    │  USB-C Power Supply (5V/3A)                     │
    │  Connected to Raspberry Pi 4B USB-C Port        │
    │  ├─ Powers main system                          │
    │  ├─ Powers DHT22 (via 3V3)                      │
    │  ├─ Powers ADS1115 (via 3V3/5V)                 │
    │  ├─ Powers Pi Camera (via GPU)                  │
    │  └─ Powers USB Webcam (via USB port)            │
    └──────────────────────────────────────────────────┘
                           ↓


    ┌─ RASPBERRY PI 4B ─────────────────────────────────┐
    │                                                   │
    │  [GPIO Header]                                   │
    │  ├─ Pin 1 (3V3) ──→ ┐                           │
    │  ├─ Pin 3 (SDA1) ──→ ├─ I2C Bus                 │
    │  ├─ Pin 5 (SCL1) ──→ ┤                           │
    │  ├─ Pin 6 (GND) ───→ ├─ Ground                  │
    │  ├─ Pin 7 (GPIO4) ─→ │ DHT22 Data              │
    │  └─ ...                                          │
    │                                                   │
    │  [CSI Camera Port] → Pi Camera Module 2          │
    │  [USB Ports] ────→ USB Webcam (fallback)        │
    │  [3.5mm Jack] ───→ Audio Output                 │
    │                                                   │
    └─────────────────────────────────────────────────-┘
            ↓                    ↓                   ↓
       ┌────────┐          ┌────────┐        ┌────────┐
       │  DHT22 │          │ADS1115 │        │ Pi Cam │
       │ Temp/  │          │  ADC   │        │ CSI   │
       │ Humid  │          └────┬───┘        └────┬──┘
       └────┬───┘               │                 │
            │              ┌────▼───┐             │
            │              │ MQ135  │             │
            │              │  AQI   │             │
            │              └────────┘             │
            │                                     │
            └─────────────────┬───────────────────┘
                              ↓
                    ┌──────────────────┐
                    │  FACE DETECTION  │
                    │  PROCESSING      │
                    │  Vision Thread   │
                    └──────────────────┘
                              ↓
                    ┌──────────────────┐
                    │  AUDIO OUTPUT    │
                    │  (3.5mm Speaker) │
                    │  TTS Playback    │
                    └──────────────────┘
```

### Detailed Pin Wiring Diagram

```
RASPBERRY PI 4B PIN-BY-PIN CONNECTION
═════════════════════════════════════════════════════════════════

                    GPIO SIDE (Top)
        ┌────────────────────────────────────┐
        │  GND  5V   GND  5V  3V3  5V   GND   │
        │  [39] [40] [38] [37] [36] [35] [34] │
        │  ┌──────────────────────────────────┐
        │  │ 1   2    3   4    5   6    7     │  ← Pin Numbers
        │  │
        └──┤
          │ POWER RAILS:
          │  ├─ 3V3 (Pin 1, 17):   For DHT22, ADS1115
          │  ├─ 5V  (Pin 2, 4):    USB webcam power
          │  └─ GND (Pin 6,9,14,20,25,30,34,39): All grounds

        
        ┌─ I2C INTERFACE (Pins 3 & 5)
        │  ├─ Pin 3 (SDA1) → ADS1115 SDA
        │  │                └─ Data line (bidirectional)
        │  └─ Pin 5 (SCL1) → ADS1115 SCL
        │                   └─ Clock line (open-drain)

        ┌─ GPIO4 (Pin 7)
        │  └─ DHT22 Data Pin
        │     └─ 1-Wire protocol (single wire + ground)

        ┌─ CSI CAMERA CONNECTOR
        │  └─ 22-pin flex cable
        │     └─ Pi Camera Module 2 (OV5647)

        └─ USB PORTS (rear panel)
           ├─ USB 3.0 port
           ├─ USB 2.0 ports
           └─ USB Webcam connected here (fallback)


EXTERNAL DEVICE CONNECTIONS
═══════════════════════════════════════════════════════════════

┌──────────────┐         ┌─────────────┐         ┌──────────┐
│   DHT22      │         │  ADS1115    │         │  MQ135   │
│              │         │             │         │          │
│ Pin1 (VCC)   │← 3V3 ─→ │ VCC         │← 3V3 ─→ │ VCC      │
│              │         │             │         │          │
│ Pin2 (Data)  │← GPIO4 │ SDA         │← Pin 3  │          │
│              │         │             │         │ A0 Analog│
│ Pin3 (NC)    │    ─    │ SCL         │← Pin 5  │          │
│              │         │             │         │          │
│ Pin4 (GND)   │← GND ─→ │ GND         │← GND ─→ │ GND      │
│              │         │             │         │          │
└──────────────┘         └─────────────┘         └──────────┘
     1-Wire              I2C Protocol               Analog Out
     (Single wire)       (2-wire bus)          (converted to I2C)


AUDIO OUTPUT CONNECTION
═════════════════════════════════════════════════════════════════

┌─ 3.5mm Jack (Raspberry Pi rear)
│  │
│  ├─ Tip (Left Channel)  ────→ Audio Amplifier (L)
│  │
│  ├─ Ring (Right Channel) ───→ Audio Amplifier (R)
│  │
│  └─ Sleeve (Ground) ────────→ Audio Amplifier GND
│
└─ Amplifier Output
   ├─ Left Speaker
   └─ Right Speaker
```

### Real-World Photo Reference

```
RASPBERRY PI 4B BACK PANEL:
┌────────────────────────────────────────┐
│                                        │
│  USB-C Power    Ethernet     Camera   │
│  Inlet          Port         Connector
│   (left)        (right)      (CSI)    │
│                             (hidden)  │
│                                        │
│  3V3V                                 │
│  3.5mm Audio Jack (LEFT CORNER)       │
│  └─ Connected to speaker/headphone    │
│                                        │
│  GPIO Header (40 pins)                │
│  Layout:                              │
│  ┌──────────────────────────────────┐ │
│  │ 1 [3V3]  2 [5V]   ... [GPIO4] 7 │ │
│  │ 3 [SDA1] 4 [5V]                  │ │
│  │ 5 [SCL1] 6 [GND] ... [GND] 40   │ │
│  └──────────────────────────────────┘ │
│                                        │
│  USB 3.0 Ports (rear, right side)     │
│  └─ USB Webcam connected here         │
│                                        │
└────────────────────────────────────────┘

FRONT PANEL:
┌────────────────────────────────────────┐
│                                        │
│  CSI Camera Connector (Top)            │
│  ├─ 22-pin flex cable slot            │
│  └─ Pi Camera Module 2 inserted        │
│     (ribbon cable goes DOWN into Pi)   │
│                                        │
│  Heatsinks (aluminum, keep cool!)     │
│  ├─ Main CPU heatsink (large)         │
│  └─ RAM heatsink (small)              │
│                                        │
└────────────────────────────────────────┘
```

---

## SENSOR CALIBRATION

### DHT22 Calibration

```python
# Code from app.py:182
t, h = dht_sensor.temperature, dht_sensor.humidity

DHT22 reads directly in standard units:
- Temperature: Already in Celsius (no conversion needed)
- Humidity: Already in % RH (0-100)

Accuracy: ±0.5°C, ±2% RH (factory calibrated)

No user calibration required.
```

### MQ135 Air Quality Calibration

```python
# Code from app.py:209
sensor_cache["aqi"] = abs(mq135.value / 32767.0 * 100)

Raw ADC Reading → Normalized AQI Scale:

┌─────────────────────────────────────────┐
│ MQ135 Raw Value  │  AQI%  │ Condition  │
├─────────────────────────────────────────┤
│     0            │   0    │ No signal  │
│  8,191 (1/4)     │  25    │ Excellent  │
│ 16,384 (1/2)     │  50    │ Good       │
│ 24,576 (3/4)     │  75    │ Moderate   │
│ 32,767 (max)     │ 100    │ Poor       │
└─────────────────────────────────────────┘

Note: This is a simplified linear mapping.
Real MQ135 requires more complex calibration:
1. Warm up for 2 minutes
2. Baseline reading in clean air (400ppm CO2)
3. Apply logarithmic calibration curve
4. But for MVP: linear scaling sufficient

To improve accuracy in production:
```python
# Production calibration (future):
def calibrate_mq135(raw_value, baseline, sensitivity):
    # Map raw value to actual ppm using curve fitting
    ppm = baseline * (raw_value / baseline) ** (1 / sensitivity)
    # Convert ppm to AQI (more complex algorithm)
    return ppm_to_aqi(ppm)
```

---

## HARDWARE CONNECTIONS REFERENCE

### Quick Connection Checklist

```
☐ STEP 1: DHT22 CONNECTION
  ├─ DHT22 Pin 1 (VCC)  → Raspberry Pi Pin 1 (3V3)
  ├─ DHT22 Pin 2 (Data) → Raspberry Pi Pin 7 (GPIO4)
  ├─ DHT22 Pin 3 (NC)   → Not connected
  └─ DHT22 Pin 4 (GND)  → Raspberry Pi Pin 6 (GND)

☐ STEP 2: ADS1115 I2C CONNECTION
  ├─ ADS1115 VCC  → Raspberry Pi Pin 1 or Pin 17 (3V3)
  ├─ ADS1115 GND  → Raspberry Pi Pin 6, 9, 14, 20, 25, 30, 34, or 39 (GND)
  ├─ ADS1115 SDA  → Raspberry Pi Pin 3 (SDA1)
  └─ ADS1115 SCL  → Raspberry Pi Pin 5 (SCL1)

☐ STEP 3: MQ135 CONNECTION TO ADS1115
  ├─ MQ135 VCC    → ADS1115 VCC (or Raspberry Pi 5V for higher sensitivity)
  ├─ MQ135 GND    → ADS1115 GND
  └─ MQ135 A0     → ADS1115 A0 (Channel 0)

☐ STEP 4: PI CAMERA CSI CONNECTION
  ├─ Locate CSI connector (between USB and Ethernet on Raspberry Pi)
  ├─ Pull back metal clips
  ├─ Insert camera flex cable
  └─ Push metal clips forward to lock

☐ STEP 5: USB WEBCAM CONNECTION
  └─ Connect USB camera to any Raspberry Pi USB 3.0 or USB 2.0 port

☐ STEP 6: AUDIO OUTPUT
  └─ Connect 3.5mm speaker/headphone to 3.5mm jack (rear left of Pi)

☐ STEP 7: POWER SUPPLY
  └─ Connect 5V/3A USB-C power to Raspberry Pi USB-C port
```

### Pinout Quick Reference Table

```
╔════════════════════════════════════════════════════════╗
║              NIKKI HARDWARE PIN QUICK REFERENCE        ║
╠════════════════════════════════════════════════════════╣
║ Component   │ Connects To  │ Pin Number │ GPIO Name   ║
╠═════════════╪══════════════╪════════════╪═════════════╣
║             │ Raspberry Pi │            │             ║
║  DHT22 VCC  │ 3V3 Power    │ Pin 1, 17  │ 3V3         ║
║  DHT22 Data │ GPIO Input   │ Pin 7      │ GPIO4       ║
║  DHT22 GND  │ Ground       │ Pin 6, etc │ GND         ║
║             │              │            │             ║
║ ADS1115 VCC │ 3V3 Power    │ Pin 1, 17  │ 3V3         ║
║ ADS1115 SDA │ I2C Data     │ Pin 3      │ SDA1        ║
║ ADS1115 SCL │ I2C Clock    │ Pin 5      │ SCL1        ║
║ ADS1115 GND │ Ground       │ Pin 6, etc │ GND         ║
║             │              │            │             ║
║  MQ135 VCC  │ ADS1115 VCC  │ ADS Pin    │ VCC         ║
║  MQ135 A0   │ ADS1115 A0   │ ADS Pin    │ Channel A0  ║
║  MQ135 GND  │ ADS1115 GND  │ ADS Pin    │ GND         ║
║             │              │            │             ║
║ Pi Camera   │ CSI Port     │ Flex Cable │ CSI         ║
║ USB Webcam  │ USB Port     │ USB 3.0    │ /dev/video0 ║
║ Audio Jack  │ 3.5mm Jack   │ Rear Left  │ Audio Out   ║
╚════════════════════════════════════════════════════════╝
```

---

## TROUBLESHOOTING

### Problem: DHT22 Not Reading

```
Symptom: sensor_cache["temp"] and sensor_cache["hum"] remain None

Diagnosis:
1. Check connection:
   ```
   $ gpio -1 readall | grep GPIO4
   Should show GPIO4 as INPUT
   ```

2. Check power:
   ```
   $ gpio -1 readall | grep 3.3V
   Should show 3.3V is powered
   ```

3. Check cable:
   ```
   Verify no loose connections
   Try with different GPIO pin (requires code change)
   ```

4. Check timing:
   ```python
   # DHT22 needs 2+ second gap between reads
   # If reads are too frequent, sensor returns cached value
   ```

Solution:
├─ Reseat cable firmly
├─ Check power supply (5V/3A minimum)
├─ Try different GPIO pin
└─ Wait 2+ seconds between reads
```

### Problem: I2C ADS1115 Not Found

```
Symptom: "Hardware Init Failed (Mock Mode)" in logs
         AQI sensor not reading

Diagnosis:
1. Check I2C bus:
   ```
   $ i2cdetect -y 1
   Shows all I2C devices on bus 1
   Should show "48" (ADS1115 address)
   ```

2. Check connections:
   ```
   Verify SDA (Pin 3) and SCL (Pin 5) connected
   Check for loose wires
   Verify pull-up resistors (4.7kΩ typical)
   ```

3. Check I2C enabled:
   ```
   $ sudo raspi-config
   Interface Options → I2C → Enable
   ```

4. Check module loaded:
   ```
   $ lsmod | grep i2c
   Should show: i2c_bcm2835
   ```

Solution:
├─ Enable I2C in raspi-config
├─ Reseat I2C cables
├─ Test with: i2cdetect -y 1
├─ Check pull-up resistors
└─ Try different I2C address (use tool: i2cset)
```

### Problem: Pi Camera (CSI) Not Working

```
Symptom: "Pi Camera failed" in logs
         Falls back to USB camera

Diagnosis:
1. Check camera enabled:
   ```
   $ sudo raspi-config
   Interface Options → Camera → Enable
   Reboot
   ```

2. Check flex cable:
   ```
   - Power off before inserting
   - Fully insert into CSI connector
   - Push metal clips forward
   - Ensure ribbon is centered
   ```

3. Check hardware:
   ```
   $ vcgencmd get_camera
   supported=1 detected=1
   (1=working, 0=problem)
   ```

4. Check permissions:
   ```
   $ ls -la /dev/video*
   Should exist (created when camera enabled)
   ```

Solution:
├─ Power off Pi
├─ Remove and reseat flex cable
├─ Ensure metal clips are locked
├─ Reboot
├─ Verify with: vcgencmd get_camera
└─ If still fails, use USB camera fallback
```

### Problem: Audio Not Playing

```
Symptom: No sound from speakers
         TTS queue processes but no audio output

Diagnosis:
1. Check audio output:
   ```
   $ aplay -L
   Lists available audio outputs
   ```

2. Check volume:
   ```
   $ alsamixer
   Ensure PCM volume is not muted/low
   ```

3. Check speaker connection:
   ```
   - Verify 3.5mm jack is plugged in
   - Try headphones to confirm
   - Check speaker power (if powered speakers)
   ```

4. Check mpg123 installed:
   ```
   $ which mpg123
   Should show: /usr/bin/mpg123
   If missing: sudo apt install mpg123
   ```

5. Test directly:
   ```
   $ echo "test" | text2speech | mpg123 -
   Should hear audio
   ```

Solution:
├─ Install mpg123: sudo apt install mpg123
├─ Check volume with alsamixer
├─ Verify speaker connection
├─ Test: python3 setup_aura_voice.py
└─ If still fails, check ALSA config
```

### Problem: High CPU Usage (>80%)

```
Symptom: Fans running constantly
         System sluggish
         Poor face detection FPS

Root Causes:
1. Resolution too high:
   ```python
   # Current: 640x480 (optimal)
   # If changed to 1920x1080: 4x CPU usage
   ```

2. Face detection too frequent:
   ```python
   # Current: time.sleep(0.1) throttling (10 FPS)
   # If removed: 100% CPU usage
   ```

3. Multiple processes running:
   ```
   ps aux | grep python
   Multiple app.py instances?
   ```

Solution:
├─ Verify resolution is 640x480
├─ Ensure throttle delay: time.sleep(0.1)
├─ Check for duplicate processes: cleanup_background()
├─ Monitor with: top
└─ If still high, reduce resolution further
```

### Problem: Memory Leak (Growing Over Time)

```
Symptom: Memory usage increases from 220MB to 500MB+ over 1-2 hours

Diagnosis:
1. Check for unreleased resources:
   ```python
   # Each frame capture = ~921KB
   # Should be released after processing
   # Check gen_frames() for buffer leaks
   ```

2. Check thread creation:
   ```
   # Only 4 daemon threads should exist
   ps -eLf | grep app.py
   ```

3. Check database growth:
   ```
   ls -lh trained_faces.pkl
   Should be stable (not growing)
   ```

Solution:
├─ Add gc.collect() in vision worker
├─ Verify threads are joining properly
├─ Monitor with: ps aux --sort=-%mem
├─ Check for infinite loops creating objects
└─ Restart app if memory >400MB
```

---

## ADVANCED DEBUGGING

### Enable Verbose Logging

```python
# app.py:12
logging.basicConfig(
    level=logging.DEBUG,  # Change from INFO to DEBUG
    format='%(asctime)s - %(levelname)s - %(message)s'
)
```

### Monitor GPIO in Real-Time

```bash
# Terminal 1: Watch GPIO changes
$ gpio -1 readall

# Terminal 2: Test DHT22 read
$ python3 -c "
from adafruit_dht import DHT22
import board
sensor = DHT22(board.D4)
print(f'Temp: {sensor.temperature}°C, Hum: {sensor.humidity}%')
"
```

### Test I2C Communication

```bash
# List all I2C devices
$ i2cdetect -y 1

# Read specific I2C device
$ i2cget -y 1 0x48
# 0x48 = ADS1115 address

# Write to I2C device
$ i2cset -y 1 0x48 0xC0 0x83
# Configure ADS1115 for single-shot read
```

### Benchmark Face Recognition Speed

```python
import time
import face_recognition

# Time a single face detection
start = time.time()
locs = face_recognition.face_locations(frame, model="hog")
elapsed = time.time() - start
print(f"Detection: {elapsed*1000:.1f}ms")

# Expected: ~100-120ms at 640x480
```

---

## POWER CONSUMPTION BREAKDOWN

```
Device Power Draw Estimates:

Raspberry Pi 4B:
├─ Idle (no peripherals):  2-3W
├─ With video streaming:   4-6W
└─ Peak (all features):    8-10W

DHT22 Sensor:
├─ Average:                ~2mA @ 3.3V ≈ 0.006W
└─ Peak:                   ~5mA @ 3.3V ≈ 0.017W

ADS1115 ADC:
├─ Idle:                   ~500µA @ 3.3V ≈ 0.0017W
└─ Sampling:               ~1mA @ 3.3V ≈ 0.0033W

MQ135 Sensor:
├─ Heating (1st hour):     ~150mW
└─ Steady state:           ~60mW

Pi Camera Module 2:
├─ Idle:                   ~30mA @ 3.3V ≈ 0.1W
└─ Capturing:              ~100mA @ 3.3V ≈ 0.33W

Audio Amplifier (typical):
├─ Idle:                   ~10mW
└─ Playing audio:          ~500mW (depends on volume)

TOTAL SYSTEM:
├─ Minimum:                ~3W
├─ Normal operation:       ~8W
└─ Peak:                   ~15W

USB-C Power Supply Rating: 5V @ 3A = 15W
Status: Adequate for all operations ✓
```

---

## LAYOUT DIAGRAM (Physical Arrangement)

```
TOP VIEW - RASPBERRY PI 4B WITH CONNECTIONS:

   Front
    ___________________________________
   |  [CSI Camera Connector]           |
   |  ├─ Pi Camera Module 2            |
   |  │  └─ Flex cable down            |
   |  │                                |
   |  | USB [USB] [USB] [USB] [USB]    |
   |  | 3.0 └─ Webcam connected here   |
   |  |      (fallback)                |
   |  |                                |
   |  |                                |
   |  |  [GPIO Header - 40 pins]       |
   |  |  ├─ DHT22 wire to Pin 7 (GPIO4)|
   |  |  ├─ I2C wires to Pins 3 & 5   |
   |  |  ├─ Ground to Pin 6             |
   |  |  └─ 3V3 power to Pin 1          |
   |  |                                |
   |  | [3.5mm]                        |
   |  | Audio Jack                     |
   |  | └─ Speaker/Headphone           |
   |  |                                |
   |__|________________________________|
        Back (toward wall)
   
Side View (Left):
   ┌─────────────────────┐
   │ [CSI Port]          │
   │                     │
   │ [GPIO Header]       │
   │ │││││││││││││││     │ ← Camera flex cable
   │ ││││││││││││││      │   goes down
   │                     │
   │ [3.5mm Jack]        │
   │ o                   │
   └─────────────────────┘
```

---

**END OF HARDWARE PINOUT & WIRING DOCUMENTATION**

*This document provides complete pin-level detail for building and troubleshooting the NIKKI system hardware.*
