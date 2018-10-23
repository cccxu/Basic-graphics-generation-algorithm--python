#!/usr/bin/env python
# coding=utf-8
from pylab import *
from matplotlib.ticker import MultipleLocator
import matplotlib.patches as patches
from matplotlib.pyplot import gcf, figure


def init(ax, x0, x1, y0, y1):
    r = max(abs(x0), abs(x1), abs(y0), abs(y1))
    r = r + 3
    ax.axis([-r, r, -r, r])
    majorlocator = MultipleLocator(1)
    ax.xaxis.set_major_locator(majorlocator)
    ax.yaxis.set_major_locator(majorlocator)
    ax.grid(True)  # x坐标轴的网格使用主刻度


def add_pixel(x, y, ax, c):
    x = round(x)
    y = round(y)
    if c == 1:
        ax.add_patch(patches.Rectangle((x - 0.5, y - 0.5), 1, 1, color='b'))
        ax.plot(x, y, 'r.')
    else:
        ax.add_patch(patches.Rectangle((x - 0.5, y - 0.5), 1, 1))
        ax.plot(x, y, 'y.')


if __name__ == '__main__':
    # 将一行的字符串分割并转化为数字
    x0, y0, x1, y1 = map(int, input("输入直线的两点: ").split(' '))
    # 确保x0的值比较小，即绘图顺序为左到右
    if x0 > x1:
        x0, x1 = x1, x0
        y0, y1 = y1, y0
    fig = gcf()
    fig.set_size_inches(19.2, 10.8)
    ax = subplot(131, aspect='equal',
                 title='modified Bresenham')  # 改进的bresenham
    ax.plot([x0, x1], [y0, y1], '-k')
    bx = subplot(132, aspect='equal', title='DDA')  # DDA
    bx.plot([x0, x1], [y0, y1], '-k')
    cx = subplot(133, aspect='equal', title='Middle Point')
    cx.plot([x0, x1], [y0, y1], '-k')
    # 图形初始化
    init(ax, x0, x1, y0, y1)
    init(bx, x0, x1, y0, y1)
    init(cx, x0, x1, y0, y1)
    delta_x = x1 - x0
    delta_y = y1 - y0
    d = 0
    if delta_x == 0:
        k = 999999999
    else:
        k = delta_y / delta_x
    x = round(x0)
    y = round(y0)
    '''
    DDA算法
    '''
    if 1 > k > -1:
        # X 最大位移
        while True:
            if x > x1:
                break
            add_pixel(x, y, bx, 1)
            x = x + 1
            y = y + k
    elif k >= 1:
        # Y 最大位移
        while True:
            if y > y1:
                break
            add_pixel(x, y, bx, 1)
            y = y + 1
            x = x + 1 / k
    # 因为从左向右绘制，所以此时y递减
    else:
        while True:
            if y < y1:
                break
            add_pixel(x, y, bx, 1)
            y = y - 1
            x = x - 1 / k
    '''
    Bresenham算法
    '''
    x = round(x0)
    y = round(y0)
    '''
    这里的e其实是e`，所以不同k值需要独立计算e`的变化方式
    '''
    if k > 1:
        e = -delta_y
        while True:
            if y > y1:
                break
            add_pixel(x, y, ax, 0)
            y = y + 1
            e = e + 2 * delta_x
            if e >= 0:
                x = x + 1
                e = e - 2 * delta_y
    elif k > 0:
        e = -delta_x
        while True:
            if x > x1:
                break
            add_pixel(x, y, ax, 0)
            x = x + 1
            e = e + 2 * delta_y
            if e >= 0:
                y = y + 1
                e = e - 2 * delta_x
    elif k > -1:
        e = -delta_x
        while True:
            if x > x1:
                break
            add_pixel(x, y, ax, 0)
            x = x + 1
            e = e - 2 * delta_y
            if e >= 0:
                y = y - 1
                e = e - 2 * delta_x
    else:
        delta_y = -delta_y
        e = -delta_y
        while True:
            if y < y1:
                break
            add_pixel(x, y, ax, 0)
            y = y - 1
            e = e + 2 * delta_x
            if e >= 0:
                x = x + 1
                e = e - 2 * delta_y
    '''
    中点画线算法
    '''
    a = y0 - y1
    b = x1 - x0
    x = round(x0)
    y = round(y0)
    if 0 < k < 1:
        d = 2 * a + b
        d1 = 2 * a
        d2 = 2 * (a + b)
        while x <= x1:
            add_pixel(x, y, cx, 3)
            if d < 0:
                x = x + 1
                y = y + 1
                d = d + d2
            else:
                x = x + 1
                d = d + d1
    elif -1 < k < 0:
        d = 2 * a - b
        d1 = 2 * (a - b)
        d2 = 2 * a
        while x <= x1:
            add_pixel(x, y, cx, 3)
            if d < 0:
                x = x + 1
                d = d + d2
            else:
                x = x + 1
                y = y - 1
                d = d + d1
    elif k > 1:
        d = a + 2 * b
        d1 = 2 * (a + b)
        d2 = 2 * b
        while y <= y1:
            add_pixel(x, y, cx, 3)
            if d > 0:
                x = x + 1
                y = y + 1
                d = d + d1
            else:
                y = y + 1
                d = d + d2
    else:
        d = a - 2 * b
        d1 = -2 * b
        d2 = 2 * (a - b)
        while y >= y1:
            add_pixel(x, y, cx, 3)
            if d <= 0:
                x = x + 1
                y = y - 1
                d = d + d2
            else:
                y = y - 1
                d = d + d1

    show()
    exit()
