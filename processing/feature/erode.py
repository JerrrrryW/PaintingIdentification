import cv2
import numpy as np
from PyQt5.QtGui import QPixmap

from utils import qtpixmap_to_cvimg, cvImg_to_qtImg


def erode(qPixmapImage: QPixmap, kernel_size_num=3, start_color=(255, 255, 255), end_color=(255, 0, 0),
          num_iterations=12):
    kernel_size = (kernel_size_num, kernel_size_num)
    # 转换图像
    img = qtpixmap_to_cvimg(qPixmapImage)

    # 转换为灰度图像
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # 应用阈值函数来去除背景
    _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    cv2.imshow('thresh', thresh)

    # 定义腐蚀核
    kernel = np.ones(kernel_size, np.uint8)

    # 腐蚀图像并显示结果
    i = 0
    while np.any(thresh > 0) and i < num_iterations:
        # 计算当前层次对应的颜色
        color = np.array(start_color) + (np.array(end_color) - np.array(start_color)) * i / float(num_iterations)
        color = color.astype(np.uint8)

        thresh = cv2.erode(thresh, kernel)
        img[thresh > 0] = color
        i += 1

    cv2.imshow('Eroded Image', img)
    cv2.waitKey(0)

    return QPixmap(cvImg_to_qtImg(img))
