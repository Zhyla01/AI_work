# import ultralytics
# import cv2
#
# # дістати перший кадр з відео
# cap = cv2.VideoCapture("data/lesson8/cars.mp4")
#
# ret, img = cap.read()
# # =========
#
# # використання моделі
# model = ultralytics.YOLO("yolov8n.pt")
#
# results = model.predict(
#     img,
#     conf=0.25,  # мінімальний відсоток з яким можна визначити об'єкт
#     iou=0.75,    # якщо для двох рамок iuo менший за це число, то вважаємо що це 2 різних об'єкта
#     #classes=[0, 2]  # індекси класів(тип об'єктів) які будуть детектитись
# )
# # results -- список з результами на кожне зображення в predict
#
# # результати для першого зображення
# result = results[0]
#
# #print(result)
#
# # отримати зображення з результатами детекції
# result_img = result.plot()
#
# # словник з назвами класів
# names = result.names
#
# # рамки
# boxes = result.boxes
#
# #print(boxes)
#
# # візуалізація
# cv2.imshow('original', img)
# cv2.imshow('result', result_img)
# cv2.waitKey(0)
#
#
# # отримання рамок для об'єктів
#
# for cls, xyxy in zip(boxes.cls, boxes.xyxy):
#     # print(cls, xyxy)
#
#     # перевести все в int
#     cls = int(cls)
#     x1, y1, x2, y2 = map(int, xyxy)
#
#     #print(cls, x1, y1, x2, y2)
#
#     # отримати назву об'єкти
#     cls_name = names[cls]
#
#     # вирізати рамку з зображення
#     # Region of Interest -- область яка нас цікавить
#     roi = img[y1:y2, x1:x2]
#
#     # візуалізація
#     cv2.imshow(cls_name, roi)
#
# cv2.waitKey(0)


# import cv2
# import ultralytics
# import numpy as np
#
#
# # сегментація
#
# img = cv2.imread("data/lesson_seg/human.jpg")
#
# model = ultralytics.YOLO('yolo11n-seg.pt')
# results = model.predict(img,
#                         classes=[0])
#
# # отримати результат для першого зображення
# result = results[0]
#
# print(result)
# print(result.masks)
#
# # візуалізація
# result.show()
#
# # дістати маску
#
# masks = result.masks.data
#
# # перевести в масив numpy
# masks = masks.numpy()
#
# # змінити тип даних на bool
# masks = masks.astype(bool)
#
# # отримати маску для першого об'єкта
# mask = masks[0]
#
# print(mask)
#
# # візуалізація маски
# mask_img = mask * 255
# mask_img = mask_img.astype(np.uint8)
#
# cv2.imshow('mask', mask_img)
#
# # обрахунок площі об'єкту
# area = mask.sum()  # площа в пікселях
#
# pixel_to_meter = 0.000001
#
# area_meter = area * pixel_to_meter
# print(f"Площа в пікселях {area}")
# print(f"Площа в метрах {area_meter}")
#
# # відсоток зайнятої площі від зображення
# area_percent = mask.mean()  # середнє арифметичне
#
# print(f"Площа у відсотках {area_percent}")
#
# # інше зображення як фон
# background = cv2.imread("data/lesson_seg/castello.png")
#
# # зробити фон та оригінальне зображення такогож розміру що й маска
# height, width = mask.shape
# background = cv2.resize(background, (width, height))
# img = cv2.resize(img, (width, height))
#
# print(img.shape)
# print(background.shape)
#
# # змінити фон
#
# new_img = img.copy()
# new_img[~mask] = 255  # зробити фон білим
#
# # змінити фон на картинку
# background[mask] = img[mask]
#
# cv2.imshow('white background', new_img)
# cv2.imshow('img background', background)
#
#
# cv2.waitKey(0)


# import cv2
# import ultralytics
#
# model = ultralytics.YOLO('yolo11n-pose.pt')
#
# img = cv2.imread('data/lesson_pose/human.jpg')
#
# results = model.predict(img)
#
# res = results[0]
#
# # result_img = res.plot()
# #
# # # вивід результатів
# # print(res)
# # print(res.keypoints)  # ключові точки
# #
# # cv2.imshow("result", result_img)
# # cv2.waitKey(0)
#
# # координати точок
# xy_coords = res.keypoints.xy
#
# # дістати координати точок для першого об'єктів
# xy_coords = xy_coords[0]
#
# # змінити масив на numpy
# xy_coords = xy_coords.numpy()
#
# # змінити тип даних на int
# xy_coords = xy_coords.astype(int)
#
# # координати правої долоні
# x, y = xy_coords[10]
#
# # намалювати круг в даній точці
# # res_img = cv2.circle(
# #     img,  # зображення на якому намалювати коло
# #     (x, y),   # координати центру кола
# #     5,       # радіус у пікселях
# #     (0, 255, 0),  # колір у bgr форматі(тут -- зелений)
# #     -1      # товщина лінії(-1 -- запоанити коло повністю)
# # )
# #
# # cv2.imshow("right arm", res_img)
# # cv2.waitKey(0)
#
#
# # # перевиріти що права долоня вища за праве коліно
# #
# # # коорлинати долоні
# # x_arm, y_arm = xy_coords[10]
# #
# # # коордлинати коліна
# # x_knee, y_knee = xy_coords[14]
# #
# # # вивід коорлинати
# # print(f"Координати долоні -- {x_arm}, {y_arm}")
# # print(f"Координати коліна -- {x_knee}, {y_knee}")
# #
# # # перевірка
# # if y_arm < y_knee:
# #     print("Долоня вище зо коліно")
# # else:
# #     print("Долоня нижче зо коліно")
#
# # перевірити чи правий плече знаходиться правіше за ліву плече
#
# x_right, y_right = xy_coords[6]
# x_left, y_left = xy_coords[5]
#
# # вивід коорлинати
# print(f"Координати лівого плеча  -- {x_left}, {y_left}")
# print(f"Координати правого плеча -- {x_right}, {y_right}")
#
# # перевірка
# if x_right > x_left:
#     text = "human back"  # людина повернута спиною
# else:
#     text = "human face"  # людина повернута до вас
#
# # нанести текст на зображення
#
# img = cv2.putText(
#     img,  # зображення на яке насти текст
#     text,   # сам текст
#     (50, 350),   # координати тексту
#     cv2.FONT_HERSHEY_SIMPLEX,   # шрифт
#     1.5,   # розмір шрифту
#     (255, 255, 255),   # колір у форматі bgr(тут -- білий)
#     2   # товщина лінії
# )
#
# cv2.imshow("", img)
# cv2.waitKey(0)

# Завдання 1
# Відкрийте відео data/lesson_pose/sitting.mp4
# Ваша задача рахувати кількість присідань.
# Отримайте перший кадр та виділіть основні точки.
# Отримайте координати однієї з долонь та лівого коліна.
# Вважайте що людина присіла, коли її рука опустилась
# нижче коліна, і піднялась коли її рука опинилась вище коліна.
# Оскільки на відео є декілька людей то обирайте ту, яка
# знаходиться найближче, тобто в якої найбільша площа
# рамки(можете потренуватись на 200-му кадрі)

import cv2
import ultralytics

model = ultralytics.YOLO('yolo11n-pose.pt')

cap = cv2.VideoCapture('data/lesson_pose/sitting.mp4')

red,imag = cap.read()
imag = cv2.resize(imag,None,fx=0.1,fy=0.1)
results = model.predict(imag)
res1 = results[0]
xy = res1.keypoints.xy.numpy()[0]
xy = xy.astype(int)
xknee, yknee = xy[14]

res_img = cv2.circle(
    imag,  # зображення на якому намалювати коло
    (xknee, yknee),   # координати центру кола
    5,       # радіус у пікселях
    (0, 255, 0),  # колір у bgr форматі(тут -- зелений)
    -1      # товщина лінії(-1 -- запоанити коло повністю)
)

cv2.imshow("", res_img)
cv2.waitKey(0)


