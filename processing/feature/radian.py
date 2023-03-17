import cv2
import numpy as np
import sys


def process_image(imagePath, threshold=0, color=(0, 0, 255), thickness=2):
    img = cv2.imread(imagePath, 0)  # 读入图片
    img = np.where(img != threshold, 0, 255)
    img = img.astype("uint8")
    contours, hierarchy = cv2.findContours(img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)  # contours为轮廓集，可以计算轮廓的长度、面积等

    if len(contours) > 1:
        # 拟合椭圆
        img_copy = img.copy()
        (x_Ellipse, y_Ellipse), (a, b), angle = cv2.fitEllipse(contours[1])
        print("椭圆的短轴和长轴直径分别为" + str(a) + "和" + str(b) + "\t" + str(y_Ellipse) + ")\t" + "椭圆的旋转角度为" + str(angle))

        # 判断是否为椭圆
        cv2.ellipse(img_copy, ((x_Ellipse, y_Ellipse), (a, b), angle), color, thickness)  # 画图红色的椭圆
        cv2.imshow('img', img_copy)
        cv2.imshow('img0', img)
        cv2.waitKey(0)
    else:
        print("未检测到足够数量的轮廓")


if __name__ == '__main__':
    image_path = sys.argv[1]
    process_image(image_path)
