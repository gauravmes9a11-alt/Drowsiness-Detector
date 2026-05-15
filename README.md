#  Driver Drowsiness Detection System

> A hybrid AI + hardware safety system that detects driver drowsiness in real-time using computer vision on a laptop and a multi-sensor ESP32 module — and alerts the driver before an accident happens.

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python)
![Arduino](https://img.shields.io/badge/Arduino-ESP32-teal?logo=arduino)
![OpenCV](https://img.shields.io/badge/OpenCV-4.9-green?logo=opencv)
![MediaPipe](https://img.shields.io/badge/MediaPipe-0.10-orange)
![License](https://img.shields.io/badge/License-MIT-lightgrey)

---

##  Overview

This project combines **computer vision** (running on a laptop) with **physical sensors** (on an ESP32 microcontroller) to create a robust, low-cost drowsiness detection system. The laptop camera tracks eye closure using the Eye Aspect Ratio (EAR) algorithm via MediaPipe, while the ESP32 monitors head tilt, proximity, temperature, pulse, and vibration — triggering buzzer alerts for any anomaly.

### Key Features
- **Real-time eye tracking** using MediaPipe Face Mesh + EAR algorithm
- **Bidirectional serial communication** between laptop and ESP32
- **Multi-sensor fusion** — tilt, ultrasonic, IR, DHT11, pulse, vibration
- **Smart buzzer patterns** — different alerts for different danger levels (yawn, drowsy, SOS)
- **Calibration tool** to personalise EAR threshold to your eyes
- **Works without hardware** — camera-only mode if ESP32 is not connected

---

## Project Structure

```
drowsiness_detection/
│
├── laptop/
│   ├── drowsiness_detector.py   ← MAIN script — run this
│   ├── calibrate_ear.py         ← Calibrate EAR threshold for your eyes
│   ├── serial_monitor.py        ← Debug: view live ESP32 sensor data
│   └── requirements.txt         ← Python dependencies
│
└── esp32/
    └── esp32_main/
        └── esp32_main.ino       ← Upload to ESP32 via Arduino IDE
```

---

##  Tech Stack

| Layer | Technology |
|---|---|
| Computer Vision | OpenCV, MediaPipe Face Mesh |
| Eye Detection | Eye Aspect Ratio (EAR) algorithm |
| Microcontroller | ESP32 Dev Board |
| Sensors | HC-SR04, DHT11, IR, SW-520D, SW-420, Pulse Sensor |
| Serial Comms | PySerial (9600 baud) |
| Language | Python 3.8+, C++ (Arduino) |

---

##  Setup & Installation

### Prerequisites
- Python 3.8 or higher
- Arduino IDE (for ESP32 upload)
- A USB webcam
- ESP32 Dev Board (optional — system works in camera-only mode)

---

### Step 1 — Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/drowsiness-detection.git
cd drowsiness-detection
```

### Step 2 — Install Python Dependencies

```bash
pip install -r laptop/requirements.txt
```

### Step 3 — Upload ESP32 Code *(skip if no hardware)*

1. Open **Arduino IDE**
2. Go to `File → Open` and select `esp32/esp32_main/esp32_main.ino`
3. Install the board: `Tools → Board → ESP32 Dev Module`
4. Install library: **DHT sensor library** by Adafruit (Library Manager)
5. Select the correct COM port and click **Upload**

### Step 4 — Calibrate EAR Threshold *(recommended)*

```bash
python laptop/calibrate_ear.py
```

Follow the on-screen instructions (keep eyes open for 5s, then closed for 5s). The script will print the recommended `EAR_THRESHOLD` value — update it in `drowsiness_detector.py`.

### Step 5 — Run the System

```bash
python laptop/drowsiness_detector.py
```

> If the ESP32 is connected, update the `SERIAL_PORT` in `drowsiness_detector.py` to match your COM port (e.g. `COM3` on Windows, `/dev/ttyUSB0` on Linux/Mac).

---

## 🔌 ESP32 Wiring Diagram

```
ESP32 Pin   →   Component
──────────────────────────────────────
GPIO 34     →   Tilt Sensor (SW-520D)
GPIO 5      →   HC-SR04 TRIG
GPIO 18     →   HC-SR04 ECHO   Use voltage divider (1kΩ + 2kΩ)
GPIO 35     →   IR Proximity OUT
GPIO 4      →   DHT11 DATA  (+ 10kΩ pull-up to 3.3V)
GPIO 36     →   Pulse Sensor Signal (Analog)
GPIO 39     →   Vibration Sensor (SW-420)
GPIO 26     →   Buzzer (+) Positive
GND         →   All sensor GNDs
3.3V / 5V  →   All sensor VCC (check individual datasheets)
```

---

## 📡 Serial Communication Protocol

### Laptop → ESP32

| Command | Meaning |
|---|---|
| `DROWSY\n` | Eyes closed too long |
| `YAWN\n` | Yawn detected |
| `SAFE\n` | Driver is alert |

### ESP32 → Laptop

| Message | Meaning |
|---|---|
| `SENSORS\|DIST:...\|...` | Periodic sensor data dump |
| `ALERT\|reason` | Hardware alert triggered |
| `WARN\|reason` | Warning condition |
| `ESP32_READY` | Boot confirmation |

---

##  Buzzer Alert Patterns

| Situation | Pattern |
|---|---|
| Yawn detected | 2 medium beeps |
| Eyes closed (drowsy) | 5 rapid beeps |
| Tilt + Drowsy | SOS pattern (· · · — — — · · ·) |
| High temperature | 2 long beeps |
| Pulse anomaly | 3 medium beeps |

---

## 🔧 Configuration Reference

Open `laptop/drowsiness_detector.py` and adjust these parameters:

| Parameter | Default | Description |
|---|---|---|
| `EAR_THRESHOLD` | `0.25` | Eye closure threshold (calibrate first!) |
| `EAR_CONSEC_FRAMES` | `20` | Frames of closed eyes before alert |
| `YAWN_THRESHOLD` | `0.6` | Mouth Aspect Ratio threshold |
| `SERIAL_PORT` | `COM3` | Change to `/dev/ttyUSB0` on Linux/Mac |
| `ALERT_COOLDOWN` | `5` | Seconds between repeated alerts |

---

##  Troubleshooting

**Camera not opening**
→ Change `cv2.VideoCapture(0)` to `(1)` or `(2)`

**Serial port not found**
→ Check Device Manager for the correct port; close any other apps using it

**Face not detected**
→ Ensure good lighting on your face; sit 30–70 cm from camera

**DHT11 reading NaN**
→ Check the 10kΩ pull-up resistor; try swapping DATA and GND pins

**High BPM / erratic pulse readings**
→ The pulse sensor requires peak detection for accuracy; current implementation uses a rolling average for basic estimation

---

##  Components List

| Component | Qty |
|---|---|
| ESP32 Dev Board | 1 |
| USB Webcam | 1 |
| HC-SR04 Ultrasonic Sensor | 1 |
| IR Proximity Module | 1 |
| Tilt Sensor SW-520D | 1 |
| DHT11 Temperature Module | 1 |
| Pulse Sensor | 1 |
| Vibration Sensor SW-420 | 1 |
| Active Buzzer 5V | 1 |
| 10kΩ Resistors | 3 |
| 1kΩ + 2kΩ Resistors (voltage divider) | 1 each |
| Breadboard + Jumper Wires | — |
| USB Cable (for ESP32) | 1 |

---

##  Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss what you'd like to change.

---

##  License

This project is licensed under the [MIT License](LICENSE).

---

*Built as an MPCA project for low-cost driver safety monitoring using a hybrid AI + hardware architecture.*
