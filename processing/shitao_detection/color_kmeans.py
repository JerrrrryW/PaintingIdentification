# -*- coding: utf-8 -*-


import cv2
import numpy as np
from PIL import Image
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt

def loadData(filePath):
    f = open(filePath, 'rb') #以二进制形式打开文件
    data = []
    img = Image.open(f)  #以列表的形式返回图片像素值
    m, n = img.size   #获取图片的大小
    for i in range(m):  #将每个像素点的RGB颜色处理到0-1
        for j in range(n):
            x,y,z = img.getpixel((i,j))
            data.append([x/256.0, y/256.0, z/256.0]) #范围内并存入data
    f.close()
    return np.mat(data), m, n #以矩阵的形式返回data，以及图片大小

path = 'yuanjing.jpg'
imgData, row, col = loadData(filePath= path)
print(imgData)
print(row)
print(col)

#加载Kmeans聚类算法
km = KMeans(n_clusters= 5)

#聚类获取每个像素所属的类别
label = km.fit_predict(imgData)
label = label.reshape([row, col])
#创建一张新的灰度图保存聚类后的结果
pic_new = Image.new('L', (row, col))

#根据所属类别向图片中添加灰度值
# 最终利用聚类中心点的RGB值替换原图中每一个像素点的值，便得到了最终的分割后的图片
for i in range(row):
    for j in range(col):
        pic_new.putpixel((i, j), int(256 / (label[i][j] + 1)))
#pic_new = cv2.applyColorMap(cv2.convertScaleAbs(pic_new, alpha=-1), cv2.COLORMAP_JET)
#以JPEG格式保存图片
pic_new.save("result_demo1.jpg","JPEG")
plt.imshow(pic_new)
plt.show()


