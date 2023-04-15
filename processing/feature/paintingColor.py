import sys
import cv2
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import extcolors
from PIL import Image
from PyQt5.QtGui import QPixmap, QImage

from colormap import rgb2hex

from utils import qtpixmap_to_cvimg


def color_to_df(input):
    colors_pre_list = str(input).replace('([(', '').split(', (')[0:-1]
    df_rgb = np.array([i.split('), ')[0] + ')' for i in colors_pre_list])
    df_percent = np.array([i.split('), ')[1].replace(')', '') for i in colors_pre_list])

    # convert RGB to HEX code
    df_color_up = np.array([rgb2hex(int(i.split(", ")[0].replace("(", "")),
                           int(i.split(", ")[1]),
                           int(i.split(", ")[2].replace(")", ""))) for i in df_rgb])

    df = pd.DataFrame({'c_code': df_color_up, 'occurence': df_percent})
    return df


def extract_color(input_image: QPixmap, tolerance, limit_number):

    # Assume you have a QPixmap object named pixmap
    cv_img = qtpixmap_to_cvimg(input_image)
    cv_img = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
    pil_image = Image.fromarray(cv_img)

    # create dataframe
    colors_x = extcolors.extract_from_image(pil_image, tolerance=tolerance, limit=limit_number)
    df_color = color_to_df(colors_x)

    list_color = list(df_color['c_code'])
    list_precent = [int(i) for i in list(df_color['occurence'])]
    text_c = [' ' + str(round(p * 100 / sum(list_precent), 1)) + '%' for p in list_precent]

    fig, ax = plt.subplots(figsize=(50, 50), dpi=10)
    wedges, text = ax.pie(list_precent,
                          labels=text_c,
                          labeldistance=1.05,
                          colors=list_color,
                          textprops={'fontsize': 150, 'color': 'black'})
    plt.setp(wedges, width=0.3)
    plt.setp(wedges, width=0.36)

    ax.set_aspect("equal")
    fig.set_facecolor('white')

    # Convert the plot to QPixmap
    canvas = fig.canvas
    canvas.draw()
    data = np.frombuffer(canvas.buffer_rgba(), dtype=np.uint8)
    data = data.reshape(canvas.get_width_height()[::-1] + (4,))
    image = QImage(data, canvas.get_width_height()[0], canvas.get_width_height()[1], QImage.Format_RGBA8888)
    pixmap = QPixmap.fromImage(image)

    return pixmap


if __name__ == '__main__':
    image_path = sys.argv[1]
    extract_color(image_path, 12, 10)
