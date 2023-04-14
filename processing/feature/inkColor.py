import numpy as np
import cv2
from PyQt5.QtGui import QPixmap
from matplotlib import pyplot as plt

from utils import qtpixmap_to_cvimg, cvImg_to_qtImg


def OTSU(img_gray, GrayScale):
    assert img_gray.ndim == 2, "must input a gary_img"  # shape有几个数字, ndim就是多少
    img_gray = np.array(img_gray).ravel().astype(np.uint8)
    u1 = 0.0  # 背景像素的平均灰度值
    u2 = 0.0  # 前景像素的平均灰度值
    best_u1 = 0.0
    best_u2 = 0.0
    th = 0.0

    # 总的像素数目
    PixSum = img_gray.size
    # 各个灰度值的像素数目
    PixCount = np.zeros(GrayScale)
    # 各灰度值所占总像素数的比例
    PixRate = np.zeros(GrayScale)
    # 统计各个灰度值的像素个数
    for i in range(PixSum):
        # 默认灰度图像的像素值范围为GrayScale
        Pixvalue = img_gray[i]
        PixCount[Pixvalue] = PixCount[Pixvalue] + 1

    # 确定各个灰度值对应的像素点的个数在所有的像素点中的比例。
    for j in range(GrayScale):
        PixRate[j] = PixCount[j] * 1.0 / PixSum
    Max_var = 0
    # 确定最大类间方差对应的阈值
    for i in range(1, GrayScale):  # 从1开始是为了避免w1为0.
        u1_tem = 0.0
        u2_tem = 0.0
        # 背景像素的比列
        w1 = np.sum(PixRate[:i])
        # 前景像素的比例
        w2 = 1.0 - w1
        if w1 == 0 or w2 == 0:
            pass
        else:  # 背景像素的平均灰度值
            for m in range(i):
                u1_tem = u1_tem + PixRate[m] * m
            u1 = u1_tem * 1.0 / w1
            # 前景像素的平均灰度值
            for n in range(i, GrayScale):
                u2_tem = u2_tem + PixRate[n] * n
            u2 = u2_tem / w2
            # print(u1)
            # 类间方差公式：G=w1*w2*(u1-u2)**2
            tem_var = w1 * w2 * np.power((u1 - u2), 2)
            # print(tem_var)
            # 判断当前类间方差是否为最大值。
            if Max_var < tem_var:
                Max_var = tem_var  # 深拷贝，Max_var与tem_var占用不同的内存空间。
                th = i
                best_u1 = u1
                best_u2 = u2
    return int(th), int(best_u1), int(best_u2)


# 多阈值处理
def double_threshold_processing(x):  # x 为传入的图像
    hist = cv2.calcHist([x], [0], None, [256], [0, 256])  # 图像的灰度直方图  shape = (256,1)
    grayScale = np.arange(256).reshape(1, -1)  # 灰度级 [0,255]  shape =(1,256)
    sum_pixels = x.shape[0] * x.shape[1]  # 图像总共像素点的个数
    mG = x.mean()  # 整幅图像的平均灰度

    T1, T2, varMax = 0, 0, 0.0  # 双阈值T1、T2，类间方差varMax

    for k1 in range(1, 254):  # k1范围在1 - 253之间 1 ~ L-3

        gray_G1 = grayScale[:, :k1 + 1]  # 灰度值 0~k1 的子区域G1
        hist_G1 = hist[:k1 + 1, :]  # 子区域G1的直方图 0~k1 ,对应每个灰度值的像素点
        sum_gray_G1 = np.dot(gray_G1, hist_G1)  # G1 区域所有像素点灰度值总和 = 灰度值 * 对应像素点的个数
        sum_pixels_G1 = sum(hist_G1)  # G1 像素数量
        P1 = sum_pixels_G1 / sum_pixels  # G1 像素占比
        m1 = (sum_gray_G1 / sum_pixels_G1) if sum_pixels_G1 > 0 else 0  # G1 像素的平均灰度

        for k2 in range(k1 + 1, 255):  # k2范围在 k1+1 ~ 254 之间 k1+1 ~ L-2
            gray_G3 = grayScale[:, k2:]  # 灰度值 k2~L-1 的子区域G3
            hist_G3 = hist[k2:, :]  # 子区域G3的直方图 k2~L-1 ,对应每个灰度值的像素点
            sum_gray_G3 = np.dot(gray_G3, hist_G3)  # G3 区域所有像素点灰度值总和 = 灰度值 * 对应像素点的个数
            sum_pixels_G3 = sum(hist_G3)  # G3 像素数量
            P3 = sum_pixels_G3 / sum_pixels  # G3 像素占比
            m3 = (sum_gray_G3 / sum_pixels_G3) if sum_pixels_G3 > 0 else 0  # G3 平均灰度

            P2 = 1.0 - P1 - P3  # G2 区域的像素占比
            m2 = ((mG - P1 * m1 - P3 * m3) / P2) if P2 > 0 else 0  # G2 平均灰度

            varB = P1 * (m1 - mG) ** 2 + P2 * (m2 - mG) ** 2 + P3 * (m3 - mG) ** 2  # 类间方差

            if varB > varMax:  # 保存最大的类间方差
                T1, T2, varMax = k1, k2, varB

    x[x <= T1] = 0
    x[(x > T1) & (x < T2)] = 123  # 中间的灰度，可以更改
    x[x >= T2] = 255

    return T1, T2, x

def multi_threshold_processing(pixmap: QPixmap, num_thresholds, min_threshold, max_threshold):
    x = qtpixmap_to_cvimg(pixmap)
    x = cv2.cvtColor(x, cv2.COLOR_BGR2GRAY)

    hist = cv2.calcHist([x], [0], None, [256], [0, 256])
    grayScale = np.arange(256).reshape(1, -1)
    sum_pixels = x.shape[0] * x.shape[1]
    mG = x.mean()

    thresholds = np.linspace(min_threshold, max_threshold, num_thresholds+1, dtype=int)

    thresholded_images = []
    for i in range(num_thresholds):
        T1, T2, varMax = thresholds[i], thresholds[i+1], 0.0
        for k1 in range(T1+1, T2-1):
            gray_G1 = grayScale[:, :k1 + 1]
            hist_G1 = hist[:k1 + 1, :]
            sum_gray_G1 = np.dot(gray_G1, hist_G1)
            sum_pixels_G1 = sum(hist_G1)
            P1 = sum_pixels_G1 / sum_pixels
            m1 = (sum_gray_G1 / sum_pixels_G1) if sum_pixels_G1 > 0 else 0

            for k2 in range(k1 + 1, T2):
                gray_G3 = grayScale[:, k2:]
                hist_G3 = hist[k2:, :]
                sum_gray_G3 = np.dot(gray_G3, hist_G3)
                sum_pixels_G3 = sum(hist_G3)
                P3 = sum_pixels_G3 / sum_pixels
                m3 = (sum_gray_G3 / sum_pixels_G3) if sum_pixels_G3 > 0 else 0

                P2 = 1.0 - P1 - P3
                m2 = ((mG - P1 * m1 - P3 * m3) / P2) if P2 > 0 else 0

                varB = P1 * (m1 - mG) ** 2 + P2 * (m2 - mG) ** 2 + P3 * (m3 - mG) ** 2

                if varB > varMax:
                    T1, T2, varMax = k1, k2, varB

        thresholded_image = np.zeros(x.shape, dtype=np.uint8)
        thresholded_image[(x > T1) & (x < T2)] = (i+1) * int(255 / num_thresholds)
        thresholded_images.append(thresholded_image)

    output_image = np.zeros(x.shape, dtype=np.uint8)
    for i, img in enumerate(thresholded_images):
        output_image += img

    output_image = cv2.cvtColor(output_image, cv2.COLOR_GRAY2BGR)  # 转换回3通道图像

    return QPixmap(cvImg_to_qtImg(output_image))

if __name__ == '__main__':

    img = cv2.imread('input\\painting2.jpg', 0)
    img2 = cv2.imread('false.png', 0)
    # hist是256x1数组，每个值对应于该图像中具有相应像素值的像素数
    hist = cv2.calcHist([img], [0], None, [256], [0, 256])


    # 绘制直方图
    plt.plot(hist)
    plt.show()

    th, u1, u2 = OTSU(img, 256)  # th是阈值
    img1 = img.copy()
    img1 = np.where(img1 < th, 0, 255)
    img1 = img1.astype("uint8")

    ret1, ret2, img2 = double_threshold_processing(img.copy())  # 多阈值处理
    img2 = img2.astype("uint8")

    img2 = multi_threshold_processing(img.copy(), 3, 0, 255)  # 多阈值处理

    # cv2.imshow("a_img1", img1)
    cv2.imshow("a_img2", img2)
    # cv2.imshow("a_img2",a_img2)
    # cv2.waitKey()
# https://blog.csdn.net/qq_38828370/article/details/119677748
# https://blog.csdn.net/qq_44886601/article/details/127909666 多阈值
