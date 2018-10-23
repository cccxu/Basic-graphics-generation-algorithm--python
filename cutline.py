#!/usr/bin/env python3
# coding=utf-8

import matplotlib.pyplot as plt
import numpy as np


def DDALine(image, x0, y0, x1, y1, color):
    if x0 > x1:
        x0, x1 = x1, x0
        y0, y1 = y1, y0
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


LEFT = 1  # 0001 左
RIGHT = 2  # 0010 右
BOTTOM = 4  # 0100 下
TOP = 8  # 1000 上

'''
1001 | 1000 | 1010
------------------
0001 | 0000 | 0010
------------------
0101 | 0100 | 0110
'''


def pos(x, y, window):
    left_edge = window[0][0]
    right_edge = window[1][0]
    top_edge = window[0][1]
    bottom_edge = window[2][1]
    # 判断是否在边界上
    if ((x == left_edge or x == right_edge) and bottom_edge <= y <= top_edge) or ((y == top_edge or y == bottom_edge) and left_edge <= x <= right_edge):
        return 1111
    c = 0
    if x < left_edge:
        c = c | LEFT
    if x > right_edge:
        c = c | RIGHT
    if y < bottom_edge:
        c = c | BOTTOM
    if y > top_edge:
        c = c | TOP
    return c


def middle_point_cut(image, line, window):
    for i in range(len(line)):
        [x0, y0] = line[i]
        [x1, y1] = line[(i + 1 + len(line)) % len(line)]
        print(x0, y0, x1, y1)

        # 确保 x0 在左边
        if x0 > x1:
            x0, x1 = x1, x0
            y0, y1 = y1, y0

        # 判断直线与窗口的关系
        pos0 = pos(x0, y0, window)
        pos1 = pos(x1, y1, window)
        if (pos0 == 1111 and pos1 == 0) or (pos1 == 1111 and pos0 == 0) or (pos0 == 1111 and pos1 == 1111):
            DDALine(image, x0, y0, x1, y1, False)
            return
        else:
            if pos0 == 1111:
                pos0 = 0
            elif pos1 == 1111:
                pos1 = 0

        if pos0 | pos1 == 0:  # 完全在窗口内部
            DDALine(image, x0, y0, x1, y1, False)
            return
        elif pos0 & pos1 != 0:  # 完全在窗口外部
            return
        else:  # 存在交点
            # 此时要考虑从两个端点分别迫近
            xm = x0 + int((x1 - x0) / 2)
            if xm == x0:
                return
            if y0 < y1:
                ym = y0 + int((y1 - y0) / 2)
            else:
                ym = y1 + int((y0 - y1) / 2)
            if ym == y0:
                return
            posm = pos(xm, ym, window)



if __name__ == '__main__':
    image = np.ones([150, 150])
    plt.xlim(0, 150)
    plt.ylim(0, 150)
    line = [
        [20, 20],
        [80, 100],
    ]
    window = [
        [40, 100],
        [100, 100],
        [100, 40],
        [40, 40]
    ]
    draw(image, window, False)
    middle_point_cut(image, line, window)
    plt.imshow(image, plt.cm.gray)
    plt.show()