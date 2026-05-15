"""
Serial Bridge / Monitor
Reads sensor data FROM ESP32 and displays it.
Can be run alongside the main detector or independently for debugging.
"""

import serial
import time
import threading

SERIAL_PORT = 'COM3'       # Change to '/dev/ttyUSB0' on Linux/Mac
BAUD_RATE = 9600

sensor_data = {
    "DIST": "N/A",
    "TILT": "0",
    "IR": "0",
    "TEMP": "N/A",
    "BPM": "N/A",
    "VIB": "0"
}

def parse_sensor_line(line):
    """Parse: SENSORS|DIST:45|TILT:0|IR:1|TEMP:28.5|BPM:72|VIB:0"""
    if not line.startswith("SENSORS|"):
        return
    parts = line[len("SENSORS|"):].split("|")
    for part in parts:
        if ":" in part:
            key, val = part.split(":", 1)
            sensor_data[key] = val

def display_sensors():
    """Pretty print sensor data"""
    print("\033[H\033[J", end="")  # Clear terminal
    print("=" * 45)
    print("   ESP32 SENSOR MONITOR")
    print("=" * 45)
    print(f"  Distance (Ultrasonic) : {sensor_data['DIST']} cm")
    print(f"  Tilt Sensor           : {'⚠ TILTED' if sensor_data['TILT'] == '1' else '✓ Normal'}")
    print(f"  IR Proximity          : {'✓ Driver Present' if sensor_data['IR'] == '1' else '✗ No Driver'}")
    print(f"  Temperature           : {sensor_data['TEMP']} °C")
    print(f"  Pulse (BPM)           : {sensor_data['BPM']}")
    print(f"  Vibration             : {'⚠ Abnormal' if sensor_data['VIB'] == '1' else '✓ Normal'}")
    print("=" * 45)
    print("Press Ctrl+C to exit")

def listen_serial():
    try:
        ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
        print(f"Connected to {SERIAL_PORT}")
        time.sleep(2)
        while True:
            if ser.in_waiting:
                line = ser.readline().decode('utf-8', errors='ignore').strip()
                if line:
                    if line.startswith("SENSORS|"):
                        parse_sensor_line(line)
                        display_sensors()
                    elif line.startswith("ALERT|"):
                        print(f"\n🚨 ALERT: {line[6:]}")
                    elif line.startswith("WARN|"):
                        print(f"\n⚠ WARNING: {line[5:]}")
                    else:
                        print(f"[ESP32] {line}")
    except serial.SerialException as e:
        print(f"Serial error: {e}")
    except KeyboardInterrupt:
        print("\nMonitor stopped.")

if __name__ == "__main__":
    listen_serial()
