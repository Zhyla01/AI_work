# (Завдання_1)

# Жест	Дія
# Відкрита долоня	Почати показ, очистити полотно
# Один вказівний	Наступний слайд
# Великий вбік	Попередній слайд
# Два пальці (індекс + середній)	Малювання
# (два пальці і великий вбік)	Зміна кольору (червоний → зелений → синій)
# Три пальці (індекс, середній, безіменний)	Гумка (стирає)

import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import logging
logging.getLogger('absl').setLevel(logging.ERROR)
import absl.logging
absl.logging.set_verbosity(absl.logging.ERROR)

import cv2
import numpy as np
import time
import mediapipe as mp

#Налаштування
slide_folder = "slides"
color_list = [(0, 0, 255), (0, 255, 0), (255, 0, 0)]
color_index = 0
draw_color = color_list[color_index]
gesture_start_time = 0
gesture_active = False

#Завантаження слайдів
if not os.path.exists(slide_folder):
    raise FileNotFoundError("Створи папку 'slides' з картинками (jpg/png)")

slides = [cv2.imread(f"{slide_folder}/{img}") for img in sorted(os.listdir(slide_folder)) if img.endswith(('.png', '.jpg'))]
if not slides:
    raise FileNotFoundError("У папці 'slides' немає жодного .png або .jpg слайду")

#Розміри слайда
h, w, _ = slides[0].shape
canvas = np.zeros((h, w, 3), dtype=np.uint8)

#MediaPipe
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)
slide_index = 0
last_point = None

def fingers_up(hand_landmarks):
    fingers = []

    tips = [4, 8, 12, 16, 20]
    for i in range(1, 5):
        fingers.append(hand_landmarks.landmark[tips[i]].y < hand_landmarks.landmark[tips[i]-2].y)
    thumb = hand_landmarks.landmark[4].x > hand_landmarks.landmark[3].x

    fingers.insert(0, thumb)
    return fingers

def detect_gesture(fingers):
    total = sum(fingers)
    if total == 5:
        return "open_hand"
    elif fingers[1] and not fingers[2] and not fingers[3]:
        return "next_slide"
    elif fingers[0] and not fingers[1] and not fingers[2]:
        return "prev_slide"
    elif fingers[1] and fingers[2] and not fingers[0]:
        return "draw"
    elif fingers[0] and fingers[1] and fingers[2]:
        return "change_color"
    elif fingers[1] and fingers[2] and fingers[3]:
        return "erase"
    else:
        return "none"

while True:
    ret, frame = cap.read()
    if not ret:
        break
    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)

    gesture = "none"
    if result.multi_hand_landmarks:
        hand_landmarks = result.multi_hand_landmarks[0]
        mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

        fingers = fingers_up(hand_landmarks)
        gesture = detect_gesture(fingers)

        x = int(hand_landmarks.landmark[8].x * w)
        y = int(hand_landmarks.landmark[8].y * h)

        if gesture != "none":
            if not gesture_active:
                gesture_active = True
                gesture_start_time = time.time()
            elif time.time() - gesture_start_time > 1:
                if gesture == "open_hand":
                    canvas = np.zeros((h, w, 3), dtype=np.uint8)
                elif gesture == "next_slide":
                    slide_index = min(slide_index + 1, len(slides) - 1)
                elif gesture == "prev_slide":
                    slide_index = max(slide_index - 1, 0)
                elif gesture == "change_color":
                    color_index = (color_index + 1) % len(color_list)
                    draw_color = color_list[color_index]
                gesture_active = False
        else:
            gesture_active = False

        #Малювання
        if gesture == "draw":
            if last_point:
                cv2.line(canvas, last_point, (x, y), draw_color, 5)
            last_point = (x, y)
        elif gesture == "erase":
            cv2.circle(canvas, (x, y), 20, (0, 0, 0), -1)
            last_point = None
        else:
            last_point = None

    else:
        gesture_active = False
        last_point = None

    #Об'єднання з презентацією
    slide = slides[slide_index].copy()
    mask = cv2.cvtColor(canvas, cv2.COLOR_BGR2GRAY)
    _, inv_mask = cv2.threshold(mask, 10, 255, cv2.THRESH_BINARY)
    inv_mask = cv2.cvtColor(inv_mask, cv2.COLOR_GRAY2BGR)
    slide = cv2.bitwise_and(slide, 255 - inv_mask)
    slide = cv2.bitwise_or(slide, canvas)

    #Показ
    cv2.imshow("Presentation", slide)
    cv2.imshow("Camera", frame)
    # cv2.imshow("Canvas", canvas)  # для дебагу

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()





