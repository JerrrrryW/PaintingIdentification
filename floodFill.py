import cv2
import cv2 as cv
import imutils
import numpy as np
from PyQt5.QtCore import qDebug
from PyQt5.QtGui import *
from stamp import drawOutRectgle
import sys


def floodFill(col, row, qPixmapImage: QPixmap):
    # 1.导入图片
    if qPixmapImage.isNull():
        print("ERROR: Image is NULL!")
        return
    img_org = qtpixmap_to_cvimg(qPixmapImage)

    # 2.设置参数
    seed_point = (col, row)  # 坐标
    new_val = (255, 255, 255)  # 赋新值
    lower_diff = (30, 30, 30)  # 下灰阶差
    up_diff = (30, 30, 30)  # 上灰阶差
    # mask图片
    h, w = img_org.shape[:2]
    img_mask = np.zeros([h + 2, w + 2], np.uint8)  # 需要大一点

    img_copy = img_org.copy()  # 会覆盖原图

    # 3.执行处理
    cv.floodFill(img_copy, img_mask, seed_point, new_val, lower_diff, up_diff,
                 flags=4 | (255 << 8) | cv.FLOODFILL_FIXED_RANGE)  # 模式 4连通 + 255白色 + 区域计算

    # 4.提取轮廓
    img_mask = img_mask[1:h, 1:w]  # 还原mask大小
    cnt = cv2.findContours(img_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnt = imutils.grab_contours(cnt)
    if len(cnt) == 1:
        x_min, x_max, y_min, y_max = drawOutRectgle(cnt[0])
    else:
        print("Error: Detector find more than one contours!")
    img_mini = img_org[y_min:y_max, x_min:x_max]

    # 显示结果
    # cv.imshow("img_mask", img_mask)
    # cv.imshow("img_org", img_org)
    # cv.imshow("img_result", img_mini)

    # focus_image = cv.bitwise_and(img_org, img_org, mask=img_mask)
    # cv.imshow("focus_image",focus_image)
    qt_img_mini = QPixmap(cvimg_to_qtimg(img_mini))

    cv.waitKey()
    cv.destroyAllWindows()

    return qt_img_mini


def qtpixmap_to_cvimg(qtpixmap):
    qimg = qtpixmap.toImage()
    temp_shape = (qimg.height(), qimg.bytesPerLine() * 8 // qimg.depth())
    temp_shape += (4,)
    ptr = qimg.bits()
    ptr.setsize(qimg.byteCount())
    result = np.array(ptr, dtype=np.uint8).reshape(temp_shape)
    result = result[..., :3]

    return result


def cvimg_to_qtimg(cvimg):

    height, width, depth = cvimg.shape
    cvimg = cv2.cvtColor(cvimg, cv2.COLOR_BGR2RGB)
    cvimg = QImage(cvimg.data, width, height, width * depth, QImage.Format_RGB888)

    return cvimg
