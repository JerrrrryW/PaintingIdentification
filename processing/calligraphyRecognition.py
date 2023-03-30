import cv2
import numpy as np
from PIL import Image
import os
import pytesseract


# 定义函数将图片转换为黑白图片
from pytesseract import Output


def convert_to_bw(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  # 转为灰度图像
    # 阈值二值化
    thresh, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    return binary


# 定义函数对图片进行分割
def segment_image(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  # 转为灰度图像
    _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)  # 阈值二值化
    # 轮廓检测
    contours, hierarchy = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=lambda c: c[0][0][0])  # 按照轮廓的左上角的x坐标进行排序
    images = []
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)  # 获取包围轮廓的矩形框
        char_image = image[y:y + h, x:x + w]  # 切割出矩形框内的图像
        images.append(char_image)
    return images


# 定义函数对图片进行OCR识别
def recognize_chars(image):
    text = pytesseract.image_to_string(image, lang='chi_tra_vert')  # 进行OCR识别
    return text.strip()  # 去除识别结果中的空格和换行符


# 读取原始图片
image_path = '../input/painting3_cut.jpg'
image = cv2.imread(image_path)

# 将图片转换为黑白图片
binary_image = convert_to_bw(image)
# cv2.imshow('binary_image', binary_image)
# cv2.waitKey(0)

# 对图像进行二值化处理
_, thresh = cv2.threshold(binary_image, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

# 使用 pytesseract 对图像进行文字识别
data = pytesseract.image_to_data(thresh, lang='chi_tra', output_type=Output.DICT)

# 获取每个文字的坐标和尺寸
n_boxes = len(data['level'])
for i in range(n_boxes):
    (x, y, w, h) = (data['left'][i], data['top'][i], data['width'][i], data['height'][i])
    # 在原图上绘制矩形框
    cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
    # 分割并保存每个汉字图像
    char_img = thresh[y:y + h, x:x + w]
    if char_img is not None:
        # cv2.imshow(f'char_{i}', char_img)
        print(f'char_{i}: {data["text"][i]}')
        cv2.imwrite(f'../output/chars/char_{i}.png', char_img)
    else:
        print(f'char_{i} is empty')

# 显示结果
cv2.imshow('img', image)
cv2.waitKey(0)
