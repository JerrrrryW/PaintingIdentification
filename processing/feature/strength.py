import cv2
import numpy as np

moon = cv2.imread("true.png", 0) #读取时参数为0，顺便转化为灰度图
row, column = moon.shape
moon_f = np.copy(moon)
moon_f = moon_f.astype("float") #整数转小数

gradient = np.zeros((row, column))

for x in range(row - 1):
    for y in range(column - 1):
        gx = abs(moon_f[x + 1, y] - moon_f[x, y])
        gy = abs(moon_f[x, y + 1] - moon_f[x, y])
        gradient[x, y] = gx + gy

sharp = moon_f + gradient
sharp = np.where(sharp < 0, 0, np.where(sharp > 255, 255, sharp))


gradient = gradient.astype("uint8") #小数转0-255
sharp = sharp.astype("uint8")
cv2.imshow("moon", moon)
cv2.imshow("gradient", gradient)
cv2.imshow("sharp", sharp)
cv2.waitKey()

# https://blog.csdn.net/weixin_46263207/article/details/123309502