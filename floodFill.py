import cv2 as cv
import numpy as np
from PyQt5.QtGui import *
import sys


def floodFill(col, row, qPixmapImage):
    # 1.导入图片
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

    # 4.显示结果
    cv.imshow("img_mask", img_mask)
    #cv.imshow("img_org", img_org)
    cv.imshow("img_copy", img_copy)

    # focus_image = cv.bitwise_and(img_org, img_org, mask=img_mask)
    # cv.imshow("focus_image",focus_image)

    cv.waitKey()
    cv.destroyAllWindows()


def qtpixmap_to_cvimg(qtpixmap):

    qimg = qtpixmap.toImage()
    temp_shape = (qimg.height(), qimg.bytesPerLine() * 8 // qimg.depth())
    temp_shape += (4,)
    ptr = qimg.bits()
    ptr.setsize(qimg.byteCount())
    result = np.array(ptr, dtype=np.uint8).reshape(temp_shape)
    result = result[..., :3]

    return result
