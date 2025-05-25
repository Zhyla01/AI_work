# # import numpy as np
# # import cv2
# #
# #
# # # масив
# # # array = np.array([[1, 2, 3], # перший рядок масиву
# # #                   [4, 5, 6] # другий рядок масив
# # #                   ])
# # #
# # # print(array)
# # #
# # # print(array.dtype)  # тип даних одного елемента
# # # print(array.shape)  # розмір (рядочки, стовпчики)
# # #
# # # # індексація
# # # print(array[0, 2])   # елемент рядок 0 та стовпчик 2
# # # print(array[0])      # рядок з індексом 0
# # # print(array[0:2])    # рядки з 0 по 2
# # # print(array[:, 1])   # стовпчик з індексом 1
# #
# #
# # # зображення
# # # читання
# #
# # img = cv2.imread("data/lesson1/cameraman.png", # шлях до файлу
# #                  cv2.IMREAD_GRAYSCALE          # зображення чорнобіле
# #                  )
# #
# # # print(img)
# # # print(img.dtype)
# # # print(img.shape)
# #
# # # uint8 -- ціле число в діапазоні 0 до 255
# #
# # # виведення
# # cv2.imshow("test img",  # назва зображення
# #            img)
# #
# # # головний цикл
# # cv2.waitKey(0)
# #
#
# # import numpy as np
# # import cv2
# #
# #
# # # масив
# # # array = np.array([[1, 2, 3], # перший рядок масиву
# # #                   [4, 5, 6] # другий рядок масив
# # #                   ])
# # #
# # # print(array)
# # #
# # # print(array.dtype)  # тип даних одного елемента
# # # print(array.shape)  # розмір (рядочки, стовпчики)
# # #
# # # # індексація
# # # print(array[0, 2])   # елемент рядок 0 та стовпчик 2
# # # print(array[0])      # рядок з індексом 0
# # # print(array[0:2])    # рядки з 0 по 2
# # # print(array[:, 1])   # стовпчик з індексом 1
# #
# #
# # # зображення
# # # читання
# #
# # img = cv2.imread("data/lesson1/cameraman.png", # шлях до файлу
# #                  cv2.IMREAD_GRAYSCALE          # зображення чорнобіле
# #                  )
# #
# # # print(img)
# # # print(img.dtype)
# # # print(img.shape)
# #
# # # uint8 -- ціле число в діапазоні 0 до 255
# #
# # # виведення
# # # cv2.imshow("test img",  # назва зображення
# # #            img)
# #
# # # індексаці
# # segment = img[50:200]  # рядки з 50 по 200
# #
# # print(segment)
# # print(segment.dtype)
# # print(segment.shape)
# #
# # #cv2.imshow('segment', segment)
# #
# # # збільшити всі пікселі у segment на 20
# # segment += 20
# #
# # cv2.imshow("test img",  # назва зображення
# #            img)
# #
# # # головний цикл
# # cv2.waitKey(0)
#
# # __________________________________lab
#
# # Завдання 1
# # Відкрийте зображення data/lesson1/Lenna.png
# # Виведіть на екран розмір зображення, тип даних пікселів
# # зображення та саме зображення.
# import cv2
#
# img = cv2.imread('data/lesson1/Lenna.png', cv2.IMREAD_GRAYSCALE)
#
# # print(img.dtype)
# # print(img.shape)
#
# cv2.imshow(' ', img)
#
# # cv2.waitKey(0)
#
# # Завдання 2
# # Відкрийте зображення data/lesson1/Lenna.png
# # Виведіть на екран такі частини зображення:
# #  Верхній лівий кут 100х50
# # segment1 = img[0:100, 0:50]
# # cv2.imshow('1', segment1)
# #
# # #  Нижній правий кут 140x70
# # segment2 = img[-140:, -70:]
# # cv2.imshow('2', segment2)
#
# #  Верхня половина
# # segment2 = img[:128, :]
# # cv2.imshow('3', segment2)
#
# #  Нижня половина
# # segment4 = img[128:, :]
# # cv2.imshow('4', segment4)
#
# #  Ліва половина
# # segment5 = img[:, :128]
# # cv2.imshow('5', segment5)
#
# #  Прави половина
# # segment6 = img[:, 128:]
# # cv2.imshow('6', segment6)
#
# #  Центральний квадрат 100х100
# # segment7 = img[77:-77, 77:-77]
# # cv2.imshow('7', segment7)
#
# cv2.waitKey(0)


# import cv2
# import utils
#
# img = cv2.imread("data/lesson2/marbles.png")
# # кольорове зображення у форматі bgr
#
# # print(img)
# #
# # print(img.shape)
# # print(img.dtype)
# #
# # blue = img[:, :, 0]
# # green = img[:, :, 1]
# # red = img[:, :, 2]
# #
# # # # замінити червоний та залений на 0
# # # img[:, :, 1] = 0
# # # img[:, :, 2] = 0
# #
# # # замінити синій на 0
# # img[:, :, 0] = 0
#
#
#
# cv2.imshow("image", img)
# cv2.waitKey(0)

#
# img_bgr = cv2.imread("data/lesson2/lego.jpg")
#
# # конвертація в HSV
# img_hsv = cv2.cvtColor(img_bgr,
#                        cv2.COLOR_BGR2HSV
#                        )

# print(img_hsv)
#
# print(img_hsv.shape)
# print(img_hsv.dtype)

# utils.lesson2_hsv_range(img_bgr)


# кольорова сегментація

# # конвертація в HSV
# img_hsv = cv2.cvtColor(img_bgr,
#                        cv2.COLOR_BGR2HSV
#                        )
#
# # межі червоного кольору
# lower = (0, 150, 180)
# upper = (10, 255, 255)
#
# # кольорова маска
# mask = cv2.inRange(img_hsv, lower, upper)
#
# print(mask)
# print(mask.shape)
# print(mask.dtype)
#
# cv2.imshow("mask", mask)
# cv2.imshow("original", img_bgr)
#
# cv2.waitKey(0)

#
# # підбір параметрів
# import utils
#
#
# @utils.trackbar_decorator(min_h=(0, 180), min_s=(0, 255), min_v=(0, 255),
#                           max_h=(0, 180), max_s=(0, 255), max_v=(0, 255))
# def func(img, min_h, min_s, min_v, max_h, max_s, max_v):
#     lower = (min_h, min_s, min_v)
#     upper = (max_h, max_s, max_v)
#
#     # конвертацію в hsv
#     hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
#
#     # маска
#     mask = cv2.inRange(hsv, lower, upper)
#
#     return mask
#
#
# img = cv2.imread("data/lesson2/lego.jpg")
# func(img)


# Відкрийте зображення data/lesson2/marbles.png.
# Використайте кольорову сегментацію для отримання масок до
# кульок:
#  синього кольору
#  зеленого і червоного
#  чорного
#  білого
#  усіх кульок

# img = cv2.imread("data/lesson2/marbles.png")
#
# lower = (100, 100, 100)
# upper = (125, 255, 255)
# hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
# mask = cv2.inRange(hsv, lower, upper)
# # cv2.imshow("img", img)
# # cv2.imshow("img1", mask)
# # cv2.waitKey(0)
# new_mask = mask.astype(bool)
#
# img[~new_mask] = 0
#
# cv2.imshow("img", img)
#
# cv2.waitKey(0)

# import cv2
# #
# # img = cv2.imread("data/lesson2/marbles.png")
# #
#
# # lower = (0, 0, 200)
# # upper = (180, 50, 255)
# # hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
# # mask = cv2.inRange(hsv, lower, upper)
# #
# #
# # cv2.imshow("img", img)
# # cv2.imshow("mask", mask)
# #
# # cv2.waitKey(0)
# #
# #
# # lower = (0, 0, 0)
# # upper = (180, 150, 50)
# # hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
# # mask = cv2.inRange(hsv, lower, upper)
# #
# #
# # cv2.imshow("img", img)
# # cv2.imshow("mask", mask)
# #
# # cv2.waitKey(0)
#
# #
# # lower3 = 0
# # upper3 = 45
# # gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# # mask = cv2.inRange(gray, lower3, upper3)
# #
# # cv2.imshow("img", gray)
# # cv2.imshow("mask", mask)
# #
# # cv2.waitKey(0)
#
# # шуми та згортка
# import cv2
# import numpy as np
#
# img = cv2.imread("data/lesson3/castello_noised.png")
#
#
# # згортка
# # математика - 180 балів - 60%
# # укр мова -- 170 балів -- 20%
# # анг мова -- 190 балів -- 20%
#
# # ядро згортки(фільтр згортки)
# # масив з коефіцієнтами для пікселів
#
# # kernel = np.array([[0.05, 0.1, 0.05],
# #                    [0.1,  0.4,  0.1],
# #                    [0.05, 0.1, 0.05]])
# #
# # new_img = cv2.filter2D(img,  # оригільне зображення
# #                        -1,  # згортка для кожного кольору
# #                        kernel  # ядро з коефіцієнтами
# #                        )
# #
# # cv2.imshow("result", new_img)
#
# # гаусове розмиття
#
# # new_img1 = cv2.GaussianBlur(img,  # оригільне зображення
# #                            ksize=(3, 3), # розмір ядра\фільра\рамки
# #                            sigmaX=1  # чим більше тим сильніше розмиття
# #                            )
# #
# # cv2.imshow("result1", new_img1)
# #
# # new_img100 = cv2.GaussianBlur(img,  # оригільне зображення
# #                            ksize=(3, 3), # розмір ядра\фільра\рамки
# #                            sigmaX=100  # чим більше тим сильніше розмиття
# #                            )
# #
# # cv2.imshow("result100", new_img100)
# # cv2.imshow("original", img)
#
# # # фільтри для різних sigmaX
# # kernel1D = cv2.getGaussianKernel(3, sigma=0)
# # kernel2D = kernel1D @ kernel1D.T
# #
# # print(kernel2D)
#
# # двосторонній фільтр
#
# # new_img = cv2.bilateralFilter(img,  # оригільне зображення
# #                               d=5,  # розмір ядра\фільра\рамки
# #                               sigmaColor=75,  # впливає на коефіцієнт за кольором
# #                               sigmaSpace=75,  # вплива на коефіцієнти як в гауса
# #                               )
# #
# # cv2.imshow("bilateral", new_img)
# # cv2.imshow("original", img)
# # cv2.waitKey(0)
#
#
# # бінарізація(звичайна)
#
# img = cv2.imread("data/lesson3/sudoku.jpg")
#
# # перевести в чорнобілий формат
# gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#
# # обираємо поріг
# threshold = 70
#
# # всі пікселі які менше зробити 0
# # всі пікселі які більше зробити 255
#
# result = gray.copy()
#
# mask = gray > threshold
#
# result[mask] = 255
# result[~mask] = 0
#
#
# # бінарізація(адаптивна)
# result2 = cv2.adaptiveThreshold(gray,  # оригільне зображення(чорнобіле)
#                                 255, # інтенсивність пікселів білого кольору
#                                 cv2.ADAPTIVE_THRESH_GAUSSIAN_C,  # алгоритм як рахувати threshold
#                                 cv2.THRESH_BINARY,  # тип бінарізації
#                                 11,  # розмір ядра\фільра\рамки
#                                 2,  # наскільки сильною є бінарізацію
#                                 )
#
# cv2.imshow("original", img)
# cv2.imshow("gray", gray)
# cv2.imshow("result", result)
# cv2.imshow("result2", result2)
# cv2.waitKey(0)


# Завдання 1
# Відкрийте зображення data/lesson3/notes.png
# Проведіть бінарізацію(звичайну та адаптивну) та
# покажіть результати.
#
#
#
# Спробуйте покращити результати за допомогою:
#  гаусового розмиття з розміром фільтру 3, 5, 11 та
# sigmaX 0, 1, 2, 10
#  двосторонній фільтр(bilateral) або швидке очищення
# від шуму(fastNLMeansDenoising)
#
#
#
# У всіх випадках покажіть оригінальне зображення,
# зображення після видалення шуму та результат бінарізації.


# import cv2
#
# image = cv2.imread('data/lesson3/notes.png')
#
# gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
#
# # blur = cv2.GaussianBlur(gray,(3,3),10)
# blur = cv2.bilateralFilter(gray,  # оригільне зображення
#                               d=5,  # розмір ядра\фільра\рамки
#                               sigmaColor=75,  # впливає на коефіцієнт за кольором
#                               sigmaSpace=75,  # вплива на коефіцієнти як в гауса
#                               )
#
#
# result2 = cv2.adaptiveThreshold(blur,  # оригільне зображення(чорнобіле)
#                                 255, # інтенсивність пікселів білого кольору
#                                 cv2.ADAPTIVE_THRESH_GAUSSIAN_C,  # алгоритм як рахувати threshold
#                                 cv2.THRESH_BINARY,  # тип бінарізації
#                                 11,  # розмір ядра\фільра\рамки
#                                 2,  # наскільки сильною є бінарізацію
#                                 )
#
# cv2.imshow('result2', result2)
#
# cv2.imshow('image', image)
# cv2.imshow('gray', gray)
# cv2.waitKey(0)


import cv2
import numpy as np
import utils

# в opencv кольорове зображення у форматі BGR
img = cv2.imread("data/lesson4/castello.png")

# межі шукають на чорнобілому зображені
# gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#
# kernel = np.array([[-1, 0, 1],
#                    [-2, 0, 2],
#                    [-1, 0, 1]])
#
# vert = cv2.filter2D(gray, -1, kernel)
#
# kernel = np.array([[-1, -2, -1],
#                    [0, 0, 0],
#                    [1, 2, 1]])
#
# horiz = cv2.filter2D(gray, -1, kernel)
#
# cv2.imshow("original", img)
# cv2.imshow("vertical", vert)
# cv2.imshow("horizontal", horiz)
# cv2.waitKey(0)

# пошук меж

# edged = cv2.Canny(gray,  # зображення де шукаємо межі
#                   100,  # нижня межі інтенсивності межі
#                   150   # верхня межі інтенсивності межі
#                   )
#
# cv2.imshow("original", img)
# cv2.imshow("edged", edged)
# cv2.waitKey(0)

# функція для меж

# @utils.trackbar_decorator(lower=(0, 255), upper=(0, 255))
# def func(img, lower, upper):
#     # перетворення в чорнобіле зображення
#     gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#
#     # розмити зображення
#     gray = cv2.GaussianBlur(gray,
#                             (5, 5),
#                             sigmaX=2)
#
#     # алгоритм Canny(пошук меж)
#     edged = cv2.Canny(gray, lower, upper)
#
#     return edged
#
# func(img)


img = cv2.imread("data/lesson4/j.png", cv2.IMREAD_GRAYSCALE)

# ерозія
# якщо навколо пікселя є хоча б один чорний -- то піксель стає чорним

# піксель по сусідству -- в сежах квадрату 3х3
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
eroded = cv2.erode(img, kernel)

# dilate(розширення?)
# якщо навколо пікселя є хоча б один білий -- то піксель стає білим
dilated = cv2.dilate(img, kernel)


both = cv2.erode(img, kernel)
both = cv2.dilate(both, kernel, iterations=2)

cv2.imshow("original", img)
cv2.imshow("eroded", eroded)
cv2.imshow("dilate", dilated)
cv2.imshow("both", both)
cv2.waitKey(0)
