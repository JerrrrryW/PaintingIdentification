import sys

import pandas as pd
import matplotlib.pyplot as plt
import extcolors

from colormap import rgb2hex


def color_to_df(input):
    colors_pre_list = str(input).replace('([(', '').split(', (')[0:-1]
    df_rgb = [i.split('), ')[0] + ')' for i in colors_pre_list]
    df_percent = [i.split('), ')[1].replace(')', '') for i in colors_pre_list]

    # convert RGB to HEX code
    df_color_up = [rgb2hex(int(i.split(", ")[0].replace("(", "")),
                           int(i.split(", ")[1]),
                           int(i.split(", ")[2].replace(")", ""))) for i in df_rgb]

    df = pd.DataFrame(zip(df_color_up, df_percent), columns=['c_code', 'occurence'])
    return df


def exact_color(input_image, tolerance, limit_number):
    # crate dataframe
    img_url = input_image
    colors_x = extcolors.extract_from_path(img_url, tolerance=tolerance, limit=limit_number)  # tolerance容差,limit颜色的数量
    df_color = color_to_df(colors_x)

    # df_color
    print(df_color)
    list_color = list(df_color['c_code'])
    list_precent = [int(i) for i in list(df_color['occurence'])]
    text_c = [c + ' ' + str(round(p * 100 / sum(list_precent), 1)) + '%' for c, p in zip(list_color,
                                                                                         list_precent)]
    fig, ax = plt.subplots(figsize=(90, 90), dpi=10)
    wedges, text = ax.pie(list_precent,
                          labels=text_c,
                          labeldistance=1.05,
                          colors=list_color,
                          textprops={'fontsize': 150, 'color': 'black'}
                          )
    plt.setp(wedges, width=0.3)

    # create space in the center
    plt.setp(wedges, width=0.36)

    ax.set_aspect("equal")
    fig.set_facecolor('white')
    plt.show()


if __name__ == '__main__':
    image_path = sys.argv[1]
    exact_color(image_path, 12, 10)
