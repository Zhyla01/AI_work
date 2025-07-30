# (Завдання_1)

# Жест	Дія
# Відкрита долоня	Почати показ, очистити полотно
# Один вказівний	Наступний слайд
# Великий вбік	Попередній слайд
# Два пальці (індекс + середній)	Малювання
# (два пальці і великий вбік)	Зміна кольору (червоний → зелений → синій)
# Три пальці (індекс, середній, безіменний)	Гумка (стирає)

import cv2
import numpy as np
import os
import time
import mediapipe as mp

#Параметри
slide_folder = "slides"
colors = [(0, 0, 255), (0, 255, 0), (255, 0, 0)]  # Red, Green, Blue
color_index = 0
color = colors[color_index]
eraser_thickness = 50  # товщина гумки

#MediaPipe
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

#Завантаження слайдів
slides = [cv2.imread(f"{slide_folder}/{img}") for img in sorted(os.listdir(slide_folder)) if img.endswith(('.png', '.jpg'))]
if not slides:
    raise Exception("Слайди не знайдено. Помісти зображення у папку 'slides'")
slide_index = 0

#Камера
cap = cv2.VideoCapture(0)
canvas = np.zeros_like(slides[0])
drawing = False
prev_point = None
last_gesture_time = 0
gesture_delay = 1  # секунда

#Визначення жестів
def fingers_up(hand_landmarks):
    finger_tips = [8, 12, 16, 20]
    finger_states = []

    for tip in finger_tips:
        if hand_landmarks.landmark[tip].y < hand_landmarks.landmark[tip - 2].y:
            finger_states.append(1)  # палець піднято
        else:
            finger_states.append(0)

    thumb_tip = hand_landmarks.landmark[4]
    thumb_base = hand_landmarks.landmark[2]
    thumb_extended = abs(thumb_tip.x - thumb_base.x) > 0.1

    return finger_states, thumb_extended

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)
    current_time = time.time()
    h, w, _ = frame.shape

    #Визначення жесту
    if result.multi_hand_landmarks:
        for handLms in result.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, handLms, mp_hands.HAND_CONNECTIONS)
            fingers, thumb_extended = fingers_up(handLms)
            index_finger = handLms.landmark[8]
            x, y = int(index_finger.x * w), int(index_finger.y * h)

            #Жести
            if all(fingers):  # Відкрита долоня — скинути
                if current_time - last_gesture_time > gesture_delay:
                    canvas = np.zeros_like(slides[0])
                    slide_index = 0
                    last_gesture_time = current_time

            elif fingers == [1, 0, 0, 0]:  # Вказівний палець — наступний слайд
                if current_time - last_gesture_time > gesture_delay:
                    slide_index = min(slide_index + 1, len(slides) - 1)
                    last_gesture_time = current_time

            elif fingers == [0, 0, 0, 0] and thumb_extended:  # Великий палець — попередній слайд
                if current_time - last_gesture_time > gesture_delay:
                    slide_index = max(slide_index - 1, 0)
                    last_gesture_time = current_time

            elif fingers[:3] == [1, 1, 1] and fingers[3] == 0:  # Три пальці — гумка
                if prev_point:
                    cv2.line(canvas, prev_point, (x, y), (0, 0, 0), eraser_thickness)
                prev_point = (x, y)
                cv2.circle(frame, (x, y), 20, (0, 0, 0), -1)

            elif fingers[:2] == [1, 1]:  # Вказівний + середній — малювання
                if thumb_extended:  # Зміна кольору
                    if current_time - last_gesture_time > gesture_delay:
                        color_index = (color_index + 1) % len(colors)
                        color = colors[color_index]
                        last_gesture_time = current_time
                else:
                    drawing = True
                    if prev_point:
                        cv2.line(canvas, prev_point, (x, y), color, 5)
                    prev_point = (x, y)
                    cv2.circle(frame, (x, y), 10, color, -1)

            else:
                drawing = False
                prev_point = None

    #Маска для малювання
    gray_canvas = cv2.cvtColor(canvas, cv2.COLOR_BGR2GRAY)
    _, mask = cv2.threshold(gray_canvas, 10, 255, cv2.THRESH_BINARY)
    mask_inv = cv2.bitwise_not(mask)
    slide = slides[slide_index].copy()
    slide_bg = cv2.bitwise_and(slide, slide, mask=mask_inv)
    canvas_fg = cv2.bitwise_and(canvas, canvas, mask=mask)
    combined = cv2.add(slide_bg, canvas_fg)

    #Поточний колір
    cv2.rectangle(combined, (10, 10), (60, 60), color, -1)

    #Показ результат
    cv2.imshow("Presentation", combined)
    cv2.imshow("Webcam", frame)

    key = cv2.waitKey(1)
    if key == 27:
        break

cap.release()
cv2.destroyAllWindows()






