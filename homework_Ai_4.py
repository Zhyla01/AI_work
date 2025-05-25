# (Завдання_1)

import matplotlib

matplotlib.use('TkAgg')

import cv2
import numpy as np
import matplotlib.pyplot as plt


def process_image(image_path):

    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

    if img is None:
        print(f"Не вдалося завантажити зображення: {image_path}")
        return None

    blurred = cv2.GaussianBlur(img, (5, 5), 0)

    edges = cv2.Canny(blurred, 50, 150)

    kernel = np.ones((3, 3), np.uint8)
    dilated = cv2.dilate(edges, kernel, iterations=1)
    eroded = cv2.erode(dilated, kernel, iterations=1)

    return eroded


images_paths = [
    'data/lesson4/apple.png',
    'data/lesson4/apple_noised.png',
    'data/lesson4/apple_salt_pepper.png'
]

for path in images_paths:
    result = process_image(path)
    if result is not None:
        plt.figure(figsize=(10, 4))
        plt.subplot(1, 2, 1)
        plt.title('Original')
        original_img = cv2.imread(path)
        if original_img is not None:
            plt.imshow(cv2.cvtColor(original_img, cv2.COLOR_BGR2RGB))
        else:
            plt.text(0.5, 0.5, 'Зображення не знайдено', ha='center', va='center')
        plt.axis('off')

        plt.subplot(1, 2, 2)
        plt.title('Краї та морфологія')
        plt.imshow(result, cmap='gray')
        plt.axis('off')
        plt.show()