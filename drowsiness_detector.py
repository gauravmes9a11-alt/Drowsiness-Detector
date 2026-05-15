import cv2
import mediapipe as mp
from scipy.spatial import distance
import time

# 🔌 TRY CONNECTING ARDUINO (OPTIONAL)
arduino_connected = False

try:
    import serial
    ser = serial.Serial('COM10', 9600)   # change COM port if needed
    time.sleep(2)
    arduino_connected = True
    print("✅ Arduino Connected")
except:
    print("⚠️ Arduino NOT connected → Running camera only")

# PARAMETERS
EAR_THRESHOLD = 0.25
prev_state = 0
start_time = None

# MediaPipe setup
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(max_num_faces=1)

LEFT_EYE = [362, 385, 387, 263, 373, 380]
RIGHT_EYE = [33, 160, 158, 133, 153, 144]

def eye_aspect_ratio(landmarks, eye_indices, w, h):
    coords = [(int(landmarks[i].x * w), int(landmarks[i].y * h)) for i in eye_indices]
    p1, p2, p3, p4, p5, p6 = coords

    A = distance.euclidean(p2, p6)
    B = distance.euclidean(p3, p5)
    C = distance.euclidean(p1, p4)

    return (A + B) / (2.0 * C)

# CAMERA
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    h, w = frame.shape[:2]
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(rgb)

    drowsy = False

    if results.multi_face_landmarks:
        landmarks = results.multi_face_landmarks[0].landmark

        left_ear = eye_aspect_ratio(landmarks, LEFT_EYE, w, h)
        right_ear = eye_aspect_ratio(landmarks, RIGHT_EYE, w, h)
        ear = (left_ear + right_ear) / 2.0

        # Drowsiness logic
        if ear < EAR_THRESHOLD:
            if start_time is None:
                start_time = time.time()
            elif time.time() - start_time > 1:
                drowsy = True
        else:
            start_time = None

        # Draw eye points
        for i in LEFT_EYE + RIGHT_EYE:
            x = int(landmarks[i].x * w)
            y = int(landmarks[i].y * h)
            cv2.circle(frame, (x, y), 2, (0,255,0), -1)

        cv2.putText(frame, f"EAR: {ear:.2f}", (10,30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,255,255), 2)

    # SERIAL (ONLY IF ARDUINO CONNECTED)
    current_state = 1 if drowsy else 0

    if current_state != prev_state:
        if arduino_connected:
            ser.write(b'1' if current_state else b'0')
        prev_state = current_state

    # DISPLAY (ALWAYS WORKS)
    status = "DROWSY" if drowsy else "AWAKE"
    color = (0,0,255) if drowsy else (0,255,0)

    cv2.putText(frame, status, (10,60),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)

    if drowsy:
        cv2.putText(frame, "ALERT!", (50,100),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 3)

    cv2.imshow("Drowsiness Detector", frame)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()

if arduino_connected:
    ser.close()