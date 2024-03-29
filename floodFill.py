import cv2
import imutils
import numpy as np
from PyQt5.QtCore import qDebug
from PyQt5.QtGui import *
import sys

from utils import qtpixmap_to_cvimg, cvImg_to_qtImg, drawOutRectgle, extract_object


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
    cv2.floodFill(img_copy, img_mask, seed_point, new_val, lower_diff, up_diff,
                 flags=4 | (255 << 8) | cv2.FLOODFILL_FIXED_RANGE)  # 模式 4连通 + 255白色 + 区域计算

    # 4.提取轮廓
    img_mask = img_mask[1:h+1, 1:w+1]  # 还原mask大小
    img_mini, (x, y) = extract_object(img_org, img_mask)  # 提取对象图 + 坐标

    # cv2.imshow("img_result", img_mixed)
    #
    # cv2.waitKey()
    # cv2.destroyAllWindows()

    return img_mini, img_copy, (x, y)

