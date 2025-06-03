# (Завдання_1-2)

import cv2
from ultralytics import YOLO

model = YOLO("yolov8n.pt")

video_path = r'data\lesson8\meetings.mp4'
cap = cv2.VideoCapture(video_path)

resize_width = 1080
show_video_from = False

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    height, width = frame.shape[:2]
    scale_ratio = resize_width / width
    resized_frame = cv2.resize(frame, (resize_width, int(height * scale_ratio)))

    results = model(resized_frame, verbose=False)[0]

    persons_detected = 0

    for box in results.boxes:
        class_id = int(box.cls[0])
        conf = float(box.conf[0])

        if class_id == 0 and conf > 0.2:
            persons_detected += 1
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            cv2.rectangle(resized_frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

    if persons_detected >= 5:
        show_video_from = True

    if show_video_from:
        cv2.imshow("Detection", resized_frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
