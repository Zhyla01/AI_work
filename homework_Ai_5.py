# (Завдання_1)

import cv2

# Відкриваємо відео
cap = cv2.VideoCapture('data/lesson7/meter.mp4')

# Перевірка відкриття файлу
if not cap.isOpened():
    print("Помилка відкриття файлу")
    exit()

# Отримуємо параметри відео
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = cap.get(cv2.CAP_PROP_FPS)

# Створюємо об'єкт для запису результуючого відео
fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # або 'XVID'
out = cv2.VideoWriter('processed_meter.mp4', fourcc, fps, (frame_width, frame_height), isColor=False)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Застосовуємо bilateral filter для шумозаглушення
    filtered_frame = cv2.bilateralFilter(frame, d=9, sigmaColor=100, sigmaSpace=100)

    # Перетворюємо у відтінки сірого
    gray = cv2.cvtColor(filtered_frame, cv2.COLOR_BGR2GRAY)

    # Бінаризація (порогове значення)
    _, binary = cv2.threshold(gray, 70, 255, cv2.THRESH_BINARY)

    # Зберігаємо оброблений кадр
    out.write(binary)

# Звільняємо ресурси
cap.release()
out.release()

print("Обробку завершено та збережено файл.")