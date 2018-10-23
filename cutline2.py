'''
中点分割裁剪算法

'''

import matplotlib.pyplot as plt
import numpy as np
import cmath

LEFT = 1  # 0001 左
RIGHT = 2  # 0010 右
BOTTOM = 4  # 0100 下
TOP = 8  # 1000 上

left_edge = 40
right_edge = 100
bottom_edge = 40
top_edge = 100


def DDALine(image, x0, y0, x1, y1, color):
    dx = x1 - x0
    dy = y1 - y0
    if dx != 0:
        k = dy / dx
    else:
        for i in range(y0, y0 + dy + 1):
            image[i][x0] = color
        else:
            for i in range(y1, y1 - dy + 1):
                image[i][x0] = color
        return
    if k >= 0:
        if abs(k) < 1:
            y = y0
            xmin = x0
            xmax = x1
            for i in range(xmin, xmax + 1):
                image[int(y + 0.5)][i] = color
                y = y + k
        else:
            x = x0
            if y0 < y1:
                ymin = y0
                ymax = y1
            else:
                ymin = y1
                ymax = y0
            for i in range(ymin, ymax + 1):
                image[i][int(x + 0.5)] = color
                x = x + 1.0 / k
    if k < 0:  # k<0
        if k > -1:
            y = y0
            xmin = x0
            xmax = x1
            for i in range(xmin, xmax + 1):
                image[int(y + 0.5)][i] = color
                y = y + k
        else:
            x = x1
            if y0 < y1:
                ymin = y0
                ymax = y1
            else:
                ymin = y1
                ymax = y0
            for i in range(ymin, ymax + 1):
                image[i][int(x + 0.5)] = color
                x = x + 1.0 / k


def draw(image, graph, color):
    long = len(graph)
    for i in range(long):
        [x0, y0] = graph[i]
        [x1, y1] = graph[(i + 1 + long) % long]
        if x0 > x1:
            x0, x1 = x1, x0
            y0, y1 = y1, y0

        DDALine(image, x0, y0, x1, y1, color)


def side_div(x, y):
    c = 0
    if (x < left_edge):
        c = c | LEFT
    if (x > right_edge):
        c = c | RIGHT
    if (y < bottom_edge):
        c = c | BOTTOM
    if (y > top_edge):
        c = c | TOP
    return c


'''
flag = 1 : 在同侧外部，无任何窗口内部分
flag = 2 ： 全在内部

'''


def middle_point_cutline(graphic, image):
    length = len(graphic)
    for i in range(length):
        [x1, y1] = graphic[i]
        [x2, y2] = graphic[(i + 1 + length) % length]

        flag = 0
        side1 = side_div(x1, y1)  # p1
        side2 = side_div(x2, y2)  # p2

        if side1 == 0 and side2 == 0:  # 同时为0,在窗口内部，不用裁剪
            flag = 2
        elif side1 & side2 != 0:  # 两点在同侧外部
            flag = 1
        else:
            ff = 0
            if side2 == 0:
                [xa, ya] = [x2, y2]  # 检测p2是否在窗口内部，是则为所求一端端点
                ff = 1

            while (abs(x1 - x2) > 1 or abs(y1 - y2) > 1) and ff == 0:  # 从p1出发
                x_mid = (x1 + x2) / 2
                y_mid = (y1 + y2) / 2
                side_mid = side_div(x_mid, y_mid)

                if ((y_mid == top_edge) and (left_edge <= x_mid <= right_edge)) or ((y_mid == bottom_edge) and (left_edge <= x_mid <= right_edge)):  # 中点在边界上
                    [xa, ya] = [x_mid, y_mid]
                    break
                elif side_mid == 0:  # 若中点在窗口内部
                    x1 = x_mid
                    y1 = y_mid
                elif side_mid & side2 != 0:  # 中点和p2在同一侧外面
                    x2 = x_mid
                    y2 = y_mid
                elif side_mid & side1 != 0:
                    x1 = x_mid
                    y1 = y_mid
            if abs(x1 - x2) <= 1 and abs(y1 - y2) <= 1:
                [xa, ya] = [x2, y2]

            [x1, y1] = graphic[i]
            [x2, y2] = graphic[(i + 1 + length) % length]
            fff = 0
            if side1 == 0:
                [xb, yb] = [x1, y1]  # 检测p1是否在窗口内部，则为所求一端端点
                fff = 1
            while (abs(x1 - x2) > 1 or abs(y1 - y2) > 1) and fff == 0:  # 从p2出发
                x_mid = (x1 + x2) / 2
                y_mid = (y1 + y2) / 2
                side_mid = side_div(x_mid, y_mid)
                if ((y_mid == top_edge) and (left_edge <= x_mid <= right_edge)) or ((y_mid == bottom_edge) and (left_edge <= x_mid <= right_edge)):
                    [xa, ya] = [x_mid, y_mid]
                    break
                elif side_mid == 0:  # 若中点在窗口内部
                    x2 = x_mid
                    y2 = y_mid
                elif side_mid & side1 != 0:  # 中点和p2在同一侧外面
                    x1 = x_mid
                    y1 = y_mid
                elif side_mid & side2 != 0:
                    x2 = x_mid
                    y2 = y_mid
            if abs(x1 - x2) <= 1 and abs(y1 - y2) <= 1:
                [xb, yb] = [x1, y1]
        if flag == 1:
            pass
        elif flag == 2:
            if x1 > x2:
                x1, x2 = x2, x1
                y1, y2 = y2, y1
            DDALine(image, x1, y1, x2, y2, False)
        else:
            if xa > xb:
                xa, xb = xb, xa
                ya, yb = yb, ya
            DDALine(image, int(xa + 0.5), int(ya + 0.5), int(xb + 0.5), int(yb + 0.5), False)  # 也可以减0.5，其实最好按边处理


if __name__ == '__main__':
    image = np.ones([150, 150])
    plt.xlim(0, 150)
    plt.ylim(0, 150)

    window = [
        [40, 40],
        [40, 100],
        [100, 100],
        [100, 40]
    ]

    graphic = [
        [50, 30],
        [110, 90],
        [20, 20],
        [120, 20],
        [70, 100],
        [50, 80],
        [50, 50]
    ]
    draw(image, window, False)

    middle_point_cutline(graphic, image)

    plt.imshow(image, plt.cm.gray)
    plt.show()
