# 🚗 Driver Drowsiness Detection System
### Laptop (AI) + ESP32 (Hardware) Hybrid System

---

## 📁 Project Structure

```
drowsiness_detection/
│
├── laptop/
│   ├── drowsiness_detector.py   ← MAIN script (run this)
│   ├── serial_monitor.py        ← Debug: view ESP32 sensor data
│   ├── calibrate_ear.py         ← Calibrate EAR threshold for your eyes
│   └── requirements.txt         ← Python packages
│
└── esp32/
    └── esp32_main/
        └── esp32_main.ino       ← Upload to ESP32 via Arduino IDE
```

---

## ⚙️ SETUP INSTRUCTIONS

### STEP 1 — Install Python Libraries
```bash
pip install -r requirements.txt
```

### STEP 2 — Upload ESP32 Code
1. Open **Arduino IDE**
2. Go to: `File → Open → esp32_main.ino`
3. Install board: `Tools → Board → ESP32 Dev Module`
4. Install library: **DHT sensor library** by Adafruit
5. Select correct port and upload

### STEP 3 — Calibrate EAR Threshold
```bash
python calibrate_ear.py
```
Follow on-screen instructions, then update `EAR_THRESHOLD` in `drowsiness_detector.py`

### STEP 4 — Run Main System
```bash
python drowsiness_detector.py
```

---

## 🔌 ESP32 WIRING DIAGRAM

```
ESP32 Pin    →   Component
─────────────────────────────────────────
GPIO 34      →   Tilt Sensor (SW-520D) Signal
GPIO 5       →   HC-SR04 TRIG
GPIO 18      →   HC-SR04 ECHO
GPIO 35      →   IR Proximity OUT
GPIO 4       →   DHT11 DATA
GPIO 36      →   Pulse Sensor Signal (Analog)
GPIO 39      →   Vibration Sensor (SW-420) OUT
GPIO 26      →   Buzzer (+) Positive
GND          →   All sensor GNDs
3.3V / 5V   →   All sensor VCC (check datasheet)
```

### HC-SR04 Wiring:
```
VCC  → 5V
GND  → GND
TRIG → GPIO 5
ECHO → GPIO 18 (use voltage divider: 1kΩ + 2kΩ for 3.3V protection)
```

### DHT11 Wiring:
```
VCC  → 3.3V
GND  → GND
DATA → GPIO 4 (add 10kΩ pull-up resistor to 3.3V)
```

### Pulse Sensor Wiring:
```
VCC  → 3.3V
GND  → GND
SIG  → GPIO 36 (analog input)
```

### Buzzer Wiring:
```
(+) → GPIO 26
(-) → GND
(Add NPN transistor like 2N2222 if buzzer needs 5V)
```

---

## 📡 Serial Communication Protocol

| Laptop → ESP32 | Meaning              |
|----------------|----------------------|
| `DROWSY\n`     | Eyes closed too long |
| `YAWN\n`       | Yawn detected        |
| `SAFE\n`       | Driver is alert      |

| ESP32 → Laptop        | Meaning               |
|-----------------------|-----------------------|
| `SENSORS\|DIST:...\|` | Periodic sensor dump  |
| `ALERT\|reason`       | Hardware alert fired  |
| `WARN\|reason`        | Warning condition     |
| `ESP32_READY`         | Boot confirmation     |

---

## 🔧 Configuration (drowsiness_detector.py)

| Parameter         | Default | Description                          |
|-------------------|---------|--------------------------------------|
| `EAR_THRESHOLD`   | 0.25    | Eye Aspect Ratio threshold           |
| `EAR_CONSEC_FRAMES` | 20   | Frames before drowsy alert           |
| `YAWN_THRESHOLD`  | 0.6     | Mouth Aspect Ratio threshold         |
| `SERIAL_PORT`     | COM3    | Change to /dev/ttyUSB0 on Linux/Mac  |
| `ALERT_COOLDOWN`  | 5       | Seconds between repeated alerts      |

---

## 🚨 Alert Patterns (Buzzer)

| Situation             | Pattern              |
|-----------------------|----------------------|
| Yawn detected         | 2 beeps              |
| Eyes closed (drowsy)  | 5 rapid beeps        |
| Tilt + Drowsy         | SOS pattern          |
| High temperature      | 2 long beeps         |
| Pulse anomaly         | 3 medium beeps       |

---

## 🛠️ Troubleshooting

**Camera not opening:**
- Change `cv2.VideoCapture(0)` to `VideoCapture(1)` or `VideoCapture(2)`

**Serial not connecting:**
- Check Device Manager for correct COM port
- Ensure no other app is using the port
- Try baud rate 115200 if 9600 fails

**Face not detected:**
- Ensure good lighting on face
- Sit closer to camera (30–70 cm)

**DHT11 reading NaN:**
- Check pull-up resistor (10kΩ)
- Try swapping DATA and GND pins

---

## 📦 Components Shopping List

| Component             | Quantity |
|-----------------------|----------|
| ESP32 Dev Board       | 1        |
| USB Webcam            | 1        |
| HC-SR04 Ultrasonic    | 1        |
| IR Proximity Module   | 1        |
| Tilt Sensor SW-520D   | 1        |
| DHT11 Module          | 1        |
| Pulse Sensor          | 1        |
| Vibration SW-420      | 1        |
| Active Buzzer 5V      | 1        |
| 10kΩ Resistors        | 3        |
| 1kΩ, 2kΩ Resistors   | 1 each   |
| Breadboard + Wires    | —        |
| USB Cable (ESP32)     | 1        |

---

*Developed for low-cost driver safety monitoring using hybrid AI + hardware architecture.*
