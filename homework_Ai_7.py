# (Завдання_1)

import cv2
import ultralytics
import numpy as np

img = cv2.imread('data/lesson_seg/tumor1.jpg')

model = ultralytics.YOLO('data/lesson_seg/brain-tumor-seg.pt')

results = model.predict(img)

result = results[0]
# result.show()

# створюємо маски
masks = result.masks.data
masks = masks.numpy()
masks = masks.astype(bool)

# визначаємо площу пухлини
for i, mask in enumerate(masks):
    mask = masks[i]
    area_pxl = mask.sum()
    print(f'Площа пухлини: {area_pxl} пікселей, або {area_pxl * 0.0025:.2f} см2.')

    # # візуалізація маски
    mask_img = mask * 255
    mask_img = mask_img.astype(np.uint8)

    # зробити фон та оригінальне зображення такогож розміру що й маска
    new_img = img.copy()
    new_img = cv2.resize(new_img, (mask.shape[1], mask.shape[0]))

    new_img[~mask] = 0

    if area_pxl * 0.0025 <= 10:
        print(f'Пухлина відноситься розміром {area_pxl * 0.0025:.2f} см2 відноситься до маленьких.')
        cv2.imshow('Small tumor', new_img)
    elif area_pxl * 0.0025 >= 25:
        print(f'Пухлина відноситься розміром {area_pxl * 0.0025:.2f} см2 відноситься до великих.')
        cv2.imshow('Large tumor', new_img)
    else:
        cv2.imshow('Medium tumor', new_img)
        print(f'Пухлина відноситься розміром {area_pxl * 0.0025:.2f} см2 відноситься до середніх.')


cv2.imshow(f'Tumor area: {area_pxl} pixels or {area_pxl * 0.0025:.2f} sm2.', img)
# cv2.imshow('Result', result)
cv2.waitKey(0)
