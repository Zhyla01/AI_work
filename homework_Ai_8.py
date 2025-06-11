# (Завдання_1)

import cv2
import numpy as np
from ultralytics import YOLO

def get_angle(x1, y1, x2, y2, x3, y3):
    a = np.array([x1, y1])
    b = np.array([x2, y2])
    c = np.array([x3, y3])

    ab = a - b
    cb = c - b

    dot = ab @ cb
    norm_ab = np.linalg.norm(ab)
    norm_cb = np.linalg.norm(cb)

    if norm_ab == 0 or norm_cb == 0:
        return 0

    angle = np.arccos(np.clip(dot / (norm_ab * norm_cb), -1.0, 1.0))
    angle = np.degrees(angle)
    return angle

model = YOLO('yolo11n-pose.pt')

cap = cv2.VideoCapture('data/lesson_pose/squat.mp4')

squat_count = 0
is_down = False
LOWER_ANGLE = 75
UPPER_ANGLE = 155

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.resize(frame, None, fx=0.3, fy=0.3)

    results = model.predict(frame, verbose=False)
    res1 = results[0]


    if res1.keypoints is None or len(res1.keypoints.xy) == 0:
        cv2.imshow('Squat Counter', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        continue


    xy = res1.keypoints.xy[0].cpu().numpy().astype(int)

    try:

        x1, y1 = xy[12]
        x2, y2 = xy[14]
        x3, y3 = xy[16]
    except IndexError:

        cv2.imshow('Squat Counter', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        continue

    angle = int(get_angle(x1, y1, x2, y2, x3, y3))

    for (x, y) in [(x1, y1), (x2, y2), (x3, y3)]:
        cv2.circle(frame, (x, y), 5, (0, 255, 0), -1)

    if angle < LOWER_ANGLE and not is_down:
        is_down = True
    elif angle > UPPER_ANGLE and is_down:
        squat_count += 1
        is_down = False

    cv2.putText(frame, f'Angle: {angle}', (50, 100),
                cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 255, 255), 2)
    cv2.putText(frame, f'Squats: {squat_count}', (50, 50),
                cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 255, 255), 2)

    cv2.imshow('Squat Counter', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
