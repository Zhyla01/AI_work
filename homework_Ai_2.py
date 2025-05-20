# (Завдання_1)

import cv2
import numpy as np

def trackbar_decorator(title, max_value=100):
    def decorator(func):
        def wrapper():
            def callback(val):
                processed_hsv = func(val)

                result_bgr = cv2.cvtColor(processed_hsv, cv2.COLOR_HSV2BGR)
                cv2.imshow(title, result_bgr)
            cv2.namedWindow(title)
            cv2.createTrackbar('Value', title, 0, max_value, callback)

            callback(0)

            cv2.waitKey(0)
            cv2.destroyAllWindows()
        return wrapper
    return decorator

image_path = 'data/lesson2/darken.png'
img_bgr = cv2.imread(image_path)
if img_bgr is None:
    print(f"Не вдалося завантажити зображення з шляху: {image_path}")
    exit()

img_hsv = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2HSV)
h, s, v = cv2.split(img_hsv)

v_eq = cv2.equalizeHist(v)
img_hsv_eq = cv2.merge([h, s, v_eq])
result_eq_bgr = cv2.cvtColor(img_hsv_eq, cv2.COLOR_HSV2BGR)

cv2.imshow("Histogram Equalized", result_eq_bgr)

@trackbar_decorator("Increase Brightness", max_value=50)
def increase_brightness(val):
    # Змінюємо яскравість у HSV
    factor = 1 + (val / 100.0)  # від 1 до приблизно 1.5
    v_float = v.astype(np.float32)
    v_new = v_float * factor
    v_clipped = np.clip(v_new, 0, 255).astype(np.uint8)
    hsv_modified = cv2.merge([h, s, v_clipped])
    return hsv_modified

cv2.imshow("Original BGR", img_bgr)

increase_brightness()

cv2.destroyAllWindows()