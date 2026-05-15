"""
EAR Calibration Script
Run this BEFORE the main detector to find the correct EAR threshold for YOUR eyes.
Follow the on-screen instructions.
"""

import cv2
import mediapipe as mp
import numpy as np
from scipy.spatial import distance
import time

mp_face_mesh = mp.solutions.face_mesh

LEFT_EYE_EAR  = [362, 385, 387, 263, 373, 380]
RIGHT_EYE_EAR = [33, 160, 158, 133, 153, 144]

def eye_aspect_ratio(landmarks, eye_indices, w, h):
    coords = [(int(landmarks[i].x * w), int(landmarks[i].y * h)) for i in eye_indices]
    p1, p2, p3, p4, p5, p6 = coords
    A = distance.euclidean(p2, p6)
    B = distance.euclidean(p3, p5)
    C = distance.euclidean(p1, p4)
    return (A + B) / (2.0 * C)

def calibrate():
    cap = cv2.VideoCapture(0)
    face_mesh = mp_face_mesh.FaceMesh(max_num_faces=1, min_detection_confidence=0.5)

    open_ears = []
    closed_ears = []
    phase = "OPEN"  # OPEN → CLOSED → DONE
    phase_start = time.time()
    phase_duration = 5  # seconds per phase

    print("\n=== EAR CALIBRATION ===")
    print("Phase 1: Keep eyes OPEN for 5 seconds")
    print("Phase 2: Close eyes for 5 seconds")
    print("Press Q to skip to results\n")

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frame = cv2.flip(frame, 1)
        h, w = frame.shape[:2]
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = face_mesh.process(rgb)

        elapsed = time.time() - phase_start
        remaining = max(0, phase_duration - elapsed)

        if elapsed > phase_duration:
            if phase == "OPEN":
                phase = "CLOSED"
                phase_start = time.time()
                print("Phase 2: Close your eyes for 5 seconds")
            elif phase == "CLOSED":
                phase = "DONE"
                break

        if results.multi_face_landmarks:
            lms = results.multi_face_landmarks[0].landmark
            left_ear = eye_aspect_ratio(lms, LEFT_EYE_EAR, w, h)
            right_ear = eye_aspect_ratio(lms, RIGHT_EYE_EAR, w, h)
            ear = (left_ear + right_ear) / 2.0

            if phase == "OPEN":
                open_ears.append(ear)
                color = (0, 255, 0)
                msg = f"EYES OPEN - Keep them open! ({remaining:.1f}s)"
            else:
                closed_ears.append(ear)
                color = (0, 0, 255)
                msg = f"EYES CLOSED - Keep them closed! ({remaining:.1f}s)"

            cv2.putText(frame, f"EAR: {ear:.3f}", (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)
            cv2.putText(frame, msg, (10, h - 20),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

        cv2.imshow("Calibration", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    face_mesh.close()

    # Calculate recommended threshold
    if open_ears and closed_ears:
        avg_open = np.mean(open_ears)
        avg_closed = np.mean(closed_ears)
        recommended = (avg_open + avg_closed) / 2.0

        print("\n=== CALIBRATION RESULTS ===")
        print(f"  Average EAR (Eyes Open)  : {avg_open:.3f}")
        print(f"  Average EAR (Eyes Closed): {avg_closed:.3f}")
        print(f"  Recommended Threshold    : {recommended:.3f}")
        print(f"\n  ➜ Set EAR_THRESHOLD = {recommended:.3f} in drowsiness_detector.py")
    else:
        print("Calibration incomplete. Using default threshold: 0.25")

if __name__ == "__main__":
    calibrate()
