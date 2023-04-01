import cv2
import numpy as np

# 读取图像
img = cv2.imread('..\\..\\input\\painting2_cut.jpg')

# 转换为灰度图像
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# 应用阈值函数来去除背景
_, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
cv2.imshow('thresh',thresh)

# 定义腐蚀核
kernel = np.ones((3,3), np.uint8)

# 定义起始颜色和结束颜色
start_color = np.array([255, 255, 255])
end_color = np.array([255, 0, 0])

# 腐蚀图像并显示结果
i = 0
while np.any(thresh > 0):
    # 计算当前层次对应的颜色
    color = start_color + (end_color - start_color) * i / 12.0
    color = color.astype(np.uint8)

    thresh = cv2.erode(thresh, kernel)
    img[thresh > 0] = color
    i += 1

cv2.imshow('Eroded Image', img)
cv2.waitKey(0)

cv2.destroyAllWindows()