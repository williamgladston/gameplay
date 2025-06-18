import cv2
import mediapipe as mp
import time
from pynput.keyboard import Controller

keyboard = Controller()

# ✅ Updated keys
accelerator_key = 'd'   # Gas
brake_key = 'a'         # Brake

time.sleep(2.0)
currently_pressed_key = None

mp_draw = mp.solutions.drawing_utils
mp_hand = mp.solutions.hands

tip_ids = [4, 8, 12, 16, 20]
video = cv2.VideoCapture(0)

def PressKey(key):
    keyboard.press(key)

def ReleaseKey(key):
    keyboard.release(key)

with mp_hand.Hands(min_detection_confidence=0.5,
                   min_tracking_confidence=0.5) as hands:
    while True:
        ret, image = video.read()
        if not ret:
            break

        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False
        results = hands.process(image)
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        lmList = []
        if results.multi_hand_landmarks:
            for hand_landmark in results.multi_hand_landmarks:
                for id, lm in enumerate(hand_landmark.landmark):
                    h, w, _ = image.shape
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    lmList.append([id, cx, cy])
                mp_draw.draw_landmarks(image, hand_landmark, mp_hand.HAND_CONNECTIONS)

        if lmList:
            fingers = []
            # Thumb
            fingers.append(1 if lmList[tip_ids[0]][1] > lmList[tip_ids[0] - 1][1] else 0)
            # Fingers
            for id in range(1, 5):
                fingers.append(1 if lmList[tip_ids[id]][2] < lmList[tip_ids[id] - 2][2] else 0)

            total = fingers.count(1)

            if total == 0:  # Fist → BRAKE
                cv2.rectangle(image, (20, 300), (270, 425), (0, 255, 0), cv2.FILLED)
                cv2.putText(image, "BRAKE (A)", (45, 375), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 0, 0), 5)
                if currently_pressed_key != brake_key:
                    if currently_pressed_key:
                        ReleaseKey(currently_pressed_key)
                    PressKey(brake_key)
                    currently_pressed_key = brake_key

            elif total == 5:  # Open palm → GAS
                cv2.rectangle(image, (20, 300), (270, 425), (0, 255, 0), cv2.FILLED)
                cv2.putText(image, "GAS (D)", (45, 375), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 0, 0), 5)
                if currently_pressed_key != accelerator_key:
                    if currently_pressed_key:
                        ReleaseKey(currently_pressed_key)
                    PressKey(accelerator_key)
                    currently_pressed_key = accelerator_key

            else:
                if currently_pressed_key:
                    ReleaseKey(currently_pressed_key)
                    currently_pressed_key = None
        else:
            if currently_pressed_key:
                ReleaseKey(currently_pressed_key)
                currently_pressed_key = None

        cv2.imshow("Frame", image)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

if currently_pressed_key:
    ReleaseKey(currently_pressed_key)
video.release()
cv2.destroyAllWindows()