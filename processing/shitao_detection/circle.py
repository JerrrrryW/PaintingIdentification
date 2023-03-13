import cv2
import numpy as np



img_fake = cv2.imread("big_fake.jpg")
img_real = cv2.imread("yuanjing.jpg")

#gray_fake = cv2.cvtColor(img_fake, cv2.COLOR_BGR2GRAY) #处理为灰度图
#gray_real = cv2.cvtColor(img_real, cv2.COLOR_BGR2GRAY)

#equal_fake = cv2.equalizeHist(gray_fake)
#clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8)) #局部自适应均衡化
#equal_fake = clahe.apply(gray_fake)
#equal_real = cv2.equalizeHist(gray_real)
#equal_real = clahe.apply(gray_real)

def circle_detect(image):
    # 灰度化
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # 输出图像大小，方便根据图像大小调节minRadius和maxRadius
    print(image.shape)

    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))  # 局部自适应均衡化
    img_gray = clahe.apply(gray)

    # 进行中值滤波
    img = cv2.medianBlur(img_gray, 5)

    # 霍夫变换圆检测
    circles = cv2.HoughCircles(img, cv2.HOUGH_GRADIENT, 1, 50, param1=200, param2=10, minRadius=10, maxRadius=20)
    for circle in circles[0]:
        # 圆的基本信息
        print(circle[2])
        # 坐标行列－圆心坐标 
        x = int(circle[0])
        y = int(circle[1])
        # 半径
        r = int(circle[2])
        # 在原图用指定颜色标记出圆的边界
        cv2.circle(image, (x, y), r, (0, 0, 255), -1)
        # 画出圆的圆心
        cv2.circle(image, (x, y), 5, (0, 255, 0), -1)
    cv2.namedWindow("result", 0)
    cv2.imshow("result", image)
    cv2.imwrite('circle_result.jpg', image)



circle_detect(image=img_real)



#cv2.namedWindow("result")
#cv2.imshow("input image", circle_fake)
cv2.waitKey(0)