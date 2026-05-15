# Driver Drowsiness Detection System

> A hybrid AI + hardware safety system that detects driver drowsiness in real-time using computer vision on a laptop and an Arduino-based sensor module alerting the driver before an accident happens.

## Overview

This project combines **computer vision** (running on a laptop) with **physical sensors** (on an Arduino) to create a robust, low-cost drowsiness detection system.

The laptop camera tracks eye closure in real time using the **Eye Aspect Ratio (EAR)** algorithm via MediaPipe. When drowsiness is detected, Python sends a serial signal (`1` or `0`) to the Arduino, which immediately activates a **buzzer and LED alert**. The Arduino also continuously reads an ultrasonic sensor, IR proximity sensor, and temperature sensor, sending debug data back to the laptop.

### Key Features
- **Real-time eye tracking** using MediaPipe Face Mesh + EAR algorithm
- **Serial communication** between laptop (Python) and Arduino
- **Multi-sensor monitoring** ultrasonic distance, IR proximity, temperature
- **Instant buzzer + LED alert** when drowsiness is detected
- **EAR calibration tool** to personalise the threshold to your eyes
- **Works without Arduino** camera-only mode if hardware is not connected

---

## Project Structure

```
drowsiness_detection/

laptop/
drowsiness_detector.py MAIN script (run this)
serial_monitor.py Debug: view Arduino sensor data live
calibrate_ear.py Calibrate EAR threshold for your eyes
requirements.txt Python dependencies

arduino/
Drowsiness_Arduino/
Drowsiness_Arduino.ino Upload to Arduino via Arduino IDE
```

---

## Tech Stack

| Layer | Technology |
|---|---|
| Computer Vision | OpenCV, MediaPipe Face Mesh |
| Eye Detection | Eye Aspect Ratio (EAR) algorithm |
| Microcontroller | Arduino Uno / Nano |
| Sensors | HC-SR04 Ultrasonic, IR Proximity, LM35 Temperature Sensor |
| Output | Active Buzzer, LED |
| Serial Comms | PySerial (9600 baud) |
| Language | Python 3.8+, C++ (Arduino) |

---

## Setup & Installation

### Prerequisites
- Python 3.8 or higher
- Arduino IDE
- A USB webcam
- Arduino Uno/Nano *(optional system works in camera-only mode)*

---

### Step 1 Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/drowsiness-detection.git
cd drowsiness-detection
```

### Step 2 Install Python Dependencies

```bash
pip install -r laptop/requirements.txt
```

### Step 3 Upload Arduino Code

1. Open **Arduino IDE**
2. Go to `File Open` select `arduino/Drowsiness_Arduino/Drowsiness_Arduino.ino`
3. Select your board: `Tools Board Arduino Uno` (or Nano)
4. Select the correct port: `Tools Port COMx` (Windows) or `/dev/ttyUSB0` (Linux/Mac)
5. Click **Upload**

### Step 4 Calibrate EAR Threshold *(recommended)*

```bash
python laptop/calibrate_ear.py
```

Follow the on-screen instructions keep eyes **open for 5 seconds**, then **closed for 5 seconds**. The script will print your recommended `EAR_THRESHOLD`. Update it in `drowsiness_detector.py`.

### Step 5 Run the Main System

```bash
python laptop/drowsiness_detector.py
```

> Update `SERIAL_PORT` in `drowsiness_detector.py` to match your Arduino's COM port (e.g. `COM3` on Windows, `/dev/ttyUSB0` on Linux/Mac).

---

## Arduino Wiring Diagram

```
Arduino Pin Component

Pin 9 HC-SR04 TRIG
Pin 10 HC-SR04 ECHO
Pin 8 IR Proximity OUT
Pin 6 LED (+) Positive
Pin 5 Buzzer (+) Positive
A0 LM35 Temperature Sensor OUT
GND All sensor GNDs
5V All sensor VCC
```

### HC-SR04 Wiring:
```
VCC 5V
GND GND
TRIG Pin 9
ECHO Pin 10
```

### IR Proximity Wiring:
```
VCC 5V
GND GND
OUT Pin 8
```

### LM35 Temperature Sensor Wiring:
```
VCC 5V
GND GND
OUT A0
```

### Buzzer & LED Wiring:
```
Buzzer (+) Pin 5 | Buzzer (-) GND
LED (+) Pin 6 | LED (-) GND (add 220Ω resistor)
```

> Note: The buzzer and LED are **active LOW** in this circuit they turn ON when the pin goes LOW and OFF when HIGH.

---

## Serial Communication Protocol

### Laptop (Python) Arduino

| Signal | Meaning |
|---|---|
| `1` | Drowsy detected activate buzzer + LED |
| `0` | Alert cleared turn off buzzer + LED |

### Arduino Laptop (Debug Output)

```
Distance: 45 | Proximity: 1 | Temp: 28.50
```

---

## Configuration Reference

Edit these values in `laptop/drowsiness_detector.py`:

| Parameter | Default | Description |
|---|---|---|
| `EAR_THRESHOLD` | `0.25` | Eye closure threshold (run calibration first!) |
| `SERIAL_PORT` | `COM10` | Change to `/dev/ttyUSB0` on Linux/Mac |
| `BAUD_RATE` | `9600` | Must match the Arduino code |

---

## Troubleshooting

**Camera not opening**
Change `cv2.VideoCapture(0)` to `(1)` or `(2)`

**Serial port not connecting**
Check Device Manager for the correct COM port; make sure Arduino IDE Serial Monitor is **closed** (only one app can use the port at a time)

**Face not detected**
Ensure good lighting on your face; sit 3070 cm from the camera

**Buzzer/LED not triggering**
Double-check active LOW wiring pins go LOW to turn ON; verify all GND connections

**Temperature reading incorrect**
Confirm LM35 is wired to A0; the formula `tempValue * (5.0 / 1023.0) * 100` is specific to LM35 on a 5V Arduino

---

## Components List

| Component | Quantity |
|---|---|
| Arduino Uno / Nano | 1 |
| USB Webcam | 1 |
| HC-SR04 Ultrasonic Sensor | 1 |
| IR Proximity Module | 1 |
| LM35 Temperature Sensor | 1 |
| Active Buzzer 5V | 1 |
| LED | 1 |
| 220Ω Resistor (for LED) | 1 |
| Breadboard + Jumper Wires | |
| USB Cable (for Arduino) | 1 |

---

## Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss what you'd like to change.

---

## License

This project is licensed under the [MIT License](LICENSE).

---

*Developed as an MPCA project for low-cost driver safety monitoring using a hybrid AI + hardware architecture.*
