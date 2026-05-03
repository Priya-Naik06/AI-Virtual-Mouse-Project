import cv2
import numpy as np
import pyautogui
import time
import math
from datetime import datetime
import mediapipe as mp

# ================= MEDIAPIPE SETUP =================
mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils

hands = mp_hands.Hands(
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)

# ================= SETTINGS =================
cap = cv2.VideoCapture(0,cv2.CAP_DSHOW)
screen_w, screen_h = pyautogui.size()
frameR = 100
smoothening = 6

plocX, plocY = 0, 0
clocX, clocY = 0, 0
drag = False
last_click = 0

# ================= FUNCTIONS =================
def fingers_up(lm):
    tips = [4, 8, 12, 16, 20]
    fingers = []

    fingers.append(1 if lm[4][0] > lm[3][0] else 0)  # Thumb
    for i in range(1, 5):
        fingers.append(1 if lm[tips[i]][1] < lm[tips[i]-2][1] else 0)

    return fingers

def distance(p1, p2):
    return math.hypot(p2[0]-p1[0], p2[1]-p1[1])

# ================= MAIN LOOP =================
while True:
    success, img = cap.read()
    if not success:
        break

    img = cv2.flip(img, 1)
    h, w, _ = img.shape
    rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)

    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            lm = [(int(p.x*w), int(p.y*h)) for p in hand_landmarks.landmark]
            fingers = fingers_up(lm)

            x1, y1 = lm[8]   # Index
            x2, y2 = lm[12]  # Middle
            x4, y4 = lm[4]   # Thumb

            # ========== MOVE ==========
            if fingers[1] == 1 and fingers[2] == 0:
                x = np.interp(x1, [frameR, w-frameR], [0, screen_w])
                y = np.interp(y1, [frameR, h-frameR], [0, screen_h])
                clocX = plocX + (x - plocX)/smoothening
                clocY = plocY + (y - plocY)/smoothening
                pyautogui.moveTo(clocX, clocY)
                plocX, plocY = clocX, clocY
                cv2.putText(img, "MOVE", (20,40),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)

            # ========== LEFT CLICK ==========
            if distance(lm[8], lm[4]) < 35:
                if time.time() - last_click > 0.8:
                    pyautogui.click()
                    last_click = time.time()
                    cv2.putText(img, "LEFT CLICK", (20,80),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (255,0,0), 2)

            # ========== RIGHT CLICK ==========
            if distance(lm[12], lm[4]) < 35:
                pyautogui.click(button="right")
                time.sleep(0.6)

            # ========== DRAG ==========
            if fingers[1] == 1 and fingers[2] == 1 and fingers[3] == 1:
                if not drag:
                    pyautogui.mouseDown()
                    drag = True
            else:
                if drag:
                    pyautogui.mouseUp()
                    drag = False

            # ========== SCROLL ==========
            if fingers[3] == 1 and fingers[4] == 1:
                pyautogui.scroll(40)

            # ========== SCREENSHOT ==========
            if fingers == [1,1,1,1,1]:
                name = datetime.now().strftime("screenshot_%Y%m%d_%H%M%S.png")
                pyautogui.screenshot().save(name)
                time.sleep(1)

            mp_draw.draw_landmarks(img, hand_landmarks, mp_hands.HAND_CONNECTIONS)

    cv2.imshow("AI Virtual Mouse", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
