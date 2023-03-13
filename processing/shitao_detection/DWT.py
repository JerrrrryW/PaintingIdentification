import cv2
import numpy as np
import matplotlib.pyplot as plt
# 需要安装python小波分析库PyWavelets
from pywt import dwt2, idwt2


def put(path):
    # 0是表示直接读取灰度图
    img = cv2.imread(path, 0)
    img = cv2.equalizeHist(img)

    # 对img进行haar小波变换：,haar小波
    cA, (cH, cV, cD) = dwt2(img, 'haar')
    #cA, (cH, cV, cD) = dwt2(cA, 'haar')
    #cA, (cH, cV, cD) = dwt2(cA, 'haar')


    # 小波变换之后，低频分量对应的图像：
    a = np.uint8(cA / np.max(cA) * 255)
    # 小波变换之后，水平方向高频分量对应的图像：
    b = np.uint8(cH / np.max(cH) * 255)
    # 小波变换之后，垂直平方向高频分量对应的图像：
    c = np.uint8(cV / np.max(cV) * 255)
    # 小波变换之后，对角线方向高频分量对应的图像：
    d = np.uint8(cD / np.max(cD) * 255)

    # 根据小波系数重构回去的图像
    rimg = idwt2((cA, (cH, cV, cD)), 'haar')

    cv2.namedWindow("result", 0)
    cv2.imshow("result", a)
    cv2.imwrite('dipin.jpg', a)
    cv2.imwrite('shuipinggaopin.jpg', b)
    cv2.imwrite('chuizhigaopin.jpg', c)
    cv2.imwrite('duijiaogaopin.jpg', d)



    plt.rcParams['font.sans-serif'] = ['SimHei']
    #plt.subplot(231), plt.imshow(img, 'gray'), plt.title('原始图像'), plt.axis('off')
    plt.subplot(221), plt.imshow(a, 'gray'), plt.title('低频分量'), plt.axis('off')
    plt.subplot(222), plt.imshow(b, 'gray'), plt.title('水平方向高频分量'), plt.axis('off')
    plt.subplot(223), plt.imshow(c, 'gray'), plt.title('垂直平方向高频分量'), plt.axis('off')
    plt.subplot(224), plt.imshow(d, 'gray'), plt.title('对角线方向高频分量'), plt.axis('off')
    #plt.subplot(236), plt.imshow(rimg, 'gray'), plt.title('重构图像'), plt.axis('off')

    # plt.savefig('3.new-img.jpg')
    plt.show()


# 图像处理函数，要传入路径
put(r'yuanjing.jpg')
cv2.waitKey(0)