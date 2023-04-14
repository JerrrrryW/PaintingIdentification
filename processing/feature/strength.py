import cv2
import numpy as np

import cv2
import numpy as np
from PyQt5.QtGui import QPixmap, QImage

from utils import qtpixmap_to_cvimg, cvImg_to_qtImg


def sharpen_image(input_image:QPixmap, alpha = 10):
    alpha = alpha / 10

    # Read the input image
    moon_f = qtpixmap_to_cvimg(input_image)

    # Convert the image to grayscale
    moon_f = cv2.cvtColor(moon_f, cv2.COLOR_BGR2GRAY)

    # Compute the gradient of the image
    gx = cv2.Sobel(moon_f, cv2.CV_64F, 1, 0, ksize=3)
    gy = cv2.Sobel(moon_f, cv2.CV_64F, 0, 1, ksize=3)
    gradient = cv2.convertScaleAbs(gx) + cv2.convertScaleAbs(gy)

    # Apply the gradient to the image
    sharp = cv2.addWeighted(moon_f, 1, gradient, alpha, 0)
    sharp = np.where(sharp < 0, 0, np.where(sharp > 255, 255, sharp))

    # Convert the image to uint8
    sharp = sharp.astype("uint8")

    cv2.imshow('gradient', gradient)

    # sharp = cv2.cvtColor(sharp, cv2.COLOR_GRAY2BGR)

    # Convert the image to QPixmap via QImage
    height, width = sharp.shape
    bytesPerLine = width
    qimage = QImage(sharp.data, width, height, bytesPerLine, QImage.Format_Grayscale8)
    qpixmap = QPixmap(qimage)

    return qpixmap

# https://blog.csdn.net/weixin_46263207/article/details/123309502