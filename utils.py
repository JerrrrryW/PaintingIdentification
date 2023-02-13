import cv2
import numpy as np
from PyQt5.QtGui import QImage


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

def drawOutRectgle(cont, img = None, isdrawing=False):
    # 最小外接正矩形————用于计算轮廓内每个像素灰度值(去除 矩形-外轮廓)
    cnt = cont
    st_x, st_y, width, height = cv2.boundingRect(cnt)  # 获取外接正矩形的xy
    # 对应的四个顶点(0,1,2,3) 0：左上，1：右上，2：右下，3：左下
    bound_rect = np.array([[[st_x, st_y]], [[st_x + width, st_y]],
                           [[st_x + width, st_y + height]], [[st_x, st_y + height]]])
    if isdrawing:
        cv2.drawContours(img, [bound_rect], -1, (0, 0, 255), 2)  # 绘制最小外接正矩形
    x_min, x_max, y_min, y_max = st_x, st_x + width, st_y, st_y + height  # 矩形四顶点
    # 通过每一个最小外接正矩形(四个顶点坐标)，判断矩形内累加坐标像素的灰度值，除去小于阈值的像素(在轮廓外)
    return x_min, x_max, y_min, y_max