import time
import keyboard
import pyautogui
import cv2

fas_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
cap = cv2.VideoCapture(1)
face_missing_start = None

if not cap.isOpened():
    print("Cannot open camera")
    exit()

print("The stopwatch is going to start in 5 sec so stay focused! ")
time.sleep(5)

key_detected = False

def on_key_press(event):
    global key_detected
    key_detected = True

keyboard.on_press(on_key_press)

startpos = pyautogui.position()
start_time = time.time()
try:

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Can't receive frame (stream end?). Exiting ...")
            break
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = fas_cascade.detectMultiScale(
            gray,
            scaleFactor=1.05,
            minNeighbors=6,
            minSize=(80, 80)
        )
        if len(faces) > 0:
            face_missing_start = None
            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
        else:
            if face_missing_start is None:
                face_missing_start = time.time()
            else:
                missing_time = time.time() - face_missing_start

                if missing_time >= 10:
                    print("\nFace not detected for 10 seconds ❌")
                    break
                else:
                    cv2.putText(frame,
                                "WARNING: Face not detected",
                                (50,50),
                                cv2.FONT_HERSHEY_SIMPLEX,
                                0.9,
                                (0,0,255),
                                2)
        
        cv2.imshow('Face Detection', frame)
        if cv2.waitKey(1) == ord('q'):
            break
        
        elapsed = int(time.time() - start_time)
        print(f"\r{elapsed}", end="")
        
        if pyautogui.position() != startpos:
            print("Mouse moved, exiting")
            break
        if key_detected:
            print("\nKey pressed, exiting")
            break
        time.sleep(1)


except KeyboardInterrupt:
    print("Focus session interrupted.")
    fail_count += 1
print("\nToday's Focus Report:")
print("Total Focused Time (seconds):", elapsed)