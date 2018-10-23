#! /usr/bin/env python
# coding=utf-8
from pylab import *
from matplotlib.ticker import MultipleLocator
from matplotlib.pyplot import gcf, Circle
from matplotlib.patches import Ellipse
import matplotlib.patches

def init(r, ax):
    r = r + 3
    ax.axis([-r, r, -r, r])
    majorlocator = MultipleLocator(1)
    ax.xaxis.set_major_locator(majorlocator)
    ax.yaxis.set_major_locator(majorlocator)
    ax.grid(True)  # x坐标轴的网格使用主刻度
    return ax


def add_pixel(x, y, ax):
    ax.plot(x, y, 'r.')
    ax.plot(x, -y, 'r.')
    ax.plot(-x, y, 'r.')
    ax.plot(-x, -y, 'r.')
    ax.plot(y, x, 'r.')
    ax.plot(y, -x, 'r.')
    ax.plot(-y, x, 'r.')
    ax.plot(-y, -x, 'r.')


def add_pixel2(x, y, ax):
    if flag == 1:
        x, y = y, x
    ax.plot(x, y, 'r.')
    ax.plot(x, -y, 'r.')
    ax.plot(-x, y, 'r.')
    ax.plot(-x, -y, 'r.')


'''
圆的中点算法
'''


def middle_point_circle(r, ax):
    x = 0
    y = r
    d = 1 - r
    while x <= y:
        add_pixel(x, y, ax)
        if d < 0:
            d = d + 2 * x + 3
        else:
            d = d + 2 * (x - y) + 5
            y = y - 1
        x = x + 1


'''
圆的bresenham算法
'''


def bresenham_circle(r, ax):
    x = 0
    y = r
    delta_d = 2 * (1 - r)
    while y >= 0:
        add_pixel2(x, y, ax)
        if delta_d < 0:
            x = x + 1
            if 2 * (delta_d + y) - 1 >= 0:
                y = y - 1
                delta_d = delta_d + 2 * (x - y) + 2
            else:
                delta_d = delta_d + 2 * x + 1
        elif delta_d > 0:
            y = y - 1
            if 2 * (delta_d - x) - 1 <= 0:
                x = x + 1
                delta_d = delta_d + 2 * (x - y) + 2
            else:
                delta_d = delta_d - 2 * y + 1
        else:
            x = x + 1
            y = y - 1
            delta_d = delta_d + 2 * (x - y) + 2


'''
椭圆的中点算法
'''


def middle_point_elipse(a, b, ax):
    x = 0
    y = b
    d1 = b * b + a * a * (-b + 0.25)
    # 上半部分
    while (b * b * (x + 1)) < (a * a * (y - 0.5)):
        add_pixel2(x, y, ax)
        if d1 < 0:
            d1 = d1 + b * b * (2 * x + 3)
            x = x + 1
        else:
            d1 = d1 + b * b * (2 * x + 3) + a * a * (-2 * y + 2)
            x = x + 1
            y = y - 1
    # 上半部分终点计算下半部分起点
    d2 = b * b * (x + 0.5) * (x + 0.5) + a * a * (y - 1) * (y - 1) - a * a * b * b
    # 下半部分
    while y >= 0:
        add_pixel2(x, y, ax)
        if d2 > 0:
            d2 = d2 + a * a * (-2 * y + 3)
            y = y - 1
        else:
            d2 = d2 + b * b * (2 * x + 2) + a * a * (-2 * y + 3)
            x = x + 1
            y = y - 1


if __name__ == "__main__":
    flag = 0
    the_r = int(input("输入圆的半径: "))
    a, b = map(int, input("输入长轴和短轴").split(' '))
    fig = gcf()
    fig.set_size_inches(19.2, 10.8)
    ax = subplot(131, aspect='equal', title='Middle Point Circle')
    init(the_r, ax)
    ax.add_artist(Circle((0, 0), the_r, fill=False))
    bx = subplot(132, aspect='equal', title='Bresenham Circle')
    init(the_r, bx)
    bx.add_artist(Circle((0, 0), the_r, fill=False))
    cx = subplot(133, aspect='equal', title='Elipse')
    init(b, cx)
    cx.add_artist(Ellipse((0, 0), 2*a, 2*b, fill=False))
    middle_point_circle(the_r, ax)
    bresenham_circle(the_r, bx)
    if a < b:
        a, b = b, a
        flag = 1
    middle_point_elipse(a, b, cx)
    show()
