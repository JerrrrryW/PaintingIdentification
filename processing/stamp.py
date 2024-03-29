import sys
import cv2
import imutils
import numpy as np
from PyQt5.QtGui import QPixmap

from utils import qtpixmap_to_cvimg, drawOutRectgle, cvImg_to_qtImg


# if __name__ == "__main__":
def findStamp(imgInput: QPixmap):
    # img = cv2.imread(sys.argv[1])
    img = qtpixmap_to_cvimg(imgInput)
    # 在彩色图像的情况下，解码图像将以b g r顺序存储通道。
    grid_RGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # 从RGB色彩空间转换到HSV色彩空间
    grid_HSV = cv2.cvtColor(grid_RGB, cv2.COLOR_RGB2HSV)

    # H、S、V范围一：
    lower1 = np.array([0, 43, 46])
    upper1 = np.array([10, 255, 255])
    mask1 = cv2.inRange(grid_HSV, lower1, upper1)  # mask1 为二值图像
    res1 = cv2.bitwise_and(grid_RGB, grid_RGB, mask=mask1)

    # H、S、V范围二：(HSV中红色有两个范围)
    lower2 = np.array([156, 43, 46])
    upper2 = np.array([180, 255, 255])
    mask2 = cv2.inRange(grid_HSV, lower2, upper2)
    res2 = cv2.bitwise_and(grid_RGB, grid_RGB, mask=mask2)

    # 将两个二值图像结果 相加
    mask3 = mask1 + mask2

    # 结果显示
    # cv2.imshow("mask3", mask3)
    # cv2.imshow("img", img)

    # cv2.imshow("Mask1", mask1)
    # cv2.imshow("res1", res1)
    # cv2.imshow("Mask2", mask2)
    # cv2.imshow("res2", res2)
    # cv2.imshow("grid_RGB", grid_RGB[:, :, ::-1])  # imshow()函数传入的变量也要为b g r通道顺序

    # 开闭运算[先膨胀-后腐蚀]，尝试去除噪声(去除尖端)
    img2 = mask3.copy()
    k = np.ones((4, 4), np.uint8)  # 卷积核 如(10, 10)= 10X10的矩阵(或称数组)
    thresh_open = cv2.morphologyEx(img2, cv2.MORPH_OPEN, k)  # 开运算[先膨胀-后腐蚀]
    k = np.ones((30, 30), np.uint8)  # 卷积核2
    thresh_open2 = cv2.morphologyEx(thresh_open, cv2.MORPH_CLOSE, k)  # 闭运算消除空洞
    # thresh_open2 = thresh_open

    # cv2.imshow("open operation", thresh_open)  # 暂时屏蔽
    # cv2.imshow("open operation2", thresh_open2)  # 暂时屏蔽

    cnts = cv2.findContours(thresh_open2.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)  # RETR_EXTERNAL
    cnts = imutils.grab_contours(cnts)  # 返回轮廓 contours —— cnts
    # print (cnts)

    # (6).cnts 返回的是所有轮廓，所以需要for循环来遍历每一个轮廓
    savePath = "..\\segmented_output\\stamp"
    img = img.copy()
    for i, c in enumerate(cnts):
        # 计算轮廓区域的图像矩。 在计算机视觉和图像处理中，图像矩通常用于表征图像中对象的形状。
        # 计算最小外接正矩形的四个顶点，是否绘制外矩形框
        x_min, x_max, y_min, y_max = drawOutRectgle(c, img, True)
        img_mini = img[y_min:y_max, x_min:x_max]
        # cv2.imshow("stamp" + str(i), img_mini)
        cv2.imwrite(savePath + str(i)+".jpg", img_mini)
        print(savePath + str(i)+".jpg")

    # cv2.imshow("img with rectangle", img)
    imgOutput = QPixmap(cvImg_to_qtImg(img))


    cv2.waitKey(0)
    cv2.destroyAllWindows()

    return imgOutput, cnts, savePath
