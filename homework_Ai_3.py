# (Завдання_1)

# import cv2
# import numpy as np
#
# img = cv2.imread('data/lesson3/sonet.png')
#
# blurred = cv2.GaussianBlur(img, (5, 5), 0)
#
# gray = cv2.cvtColor(blurred, cv2.COLOR_BGR2GRAY)
#
# binary_adaptive = cv2.adaptiveThreshold(
#     gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
#     cv2.THRESH_BINARY, 11, 2
# )
#
# kernel = np.ones((3, 3), np.uint8)
# cleaned = cv2.morphologyEx(binary_adaptive, cv2.MORPH_OPEN, kernel)
#
# cv2.imwrite('result_task1.png', cleaned)

# (Завдання_2)

import cv2
import numpy as np
import os

image_path = 'D:/homework/string_utils/istep/ITStep-AI/data/lesson3/sonet_noised.png'

if not os.path.exists(image_path):
    raise FileNotFoundError(f" Файл не знайдено: {image_path}")

img = cv2.imread(image_path)

if img is None:
    raise ValueError(" Не вдалося завантажити зображення. Перевір формат файлу.")

blurred = cv2.GaussianBlur(img, (5, 5), 0)

gray = cv2.cvtColor(blurred, cv2.COLOR_BGR2GRAY)

binary_adaptive = cv2.adaptiveThreshold(
    gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
    cv2.THRESH_BINARY, 11, 2
)

kernel = np.ones((2, 2), np.uint8)
cleaned = cv2.morphologyEx(binary_adaptive, cv2.MORPH_OPEN, kernel)

result_path = 'result_task2.png'
cv2.imwrite(result_path, cleaned)
print(f" Зображення оброблено та збережено як: {result_path}")



