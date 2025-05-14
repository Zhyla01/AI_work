# # (Завдання_1)
#
# import cv2
# import numpy as np
#
# img = cv2.imread('data/lesson1/Lenna.png', cv2.IMREAD_GRAYSCALE)
#
# mask = img > 128
#
# img[mask] = 255
#
# cv2.imshow('Modified Image', img)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

# (Завдання_2)

import cv2

img = cv2.imread('data/lesson1/baboo.jpg')

if img is None:
    print("Зображення не знайдено або неправильний шлях")
else:

    segment1 = img[10:-210, 65:-65]
    cv2.imshow('1', segment1)

    cv2.imshow('Зображення baboo', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()