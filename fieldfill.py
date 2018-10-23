#!/usr/bin/env python3
# coding=utf-8

from PIL import Image
import sys

im = Image.open('./imgs/1.bmp')

'''
X, y:种子点，需要在填充区域内部
Filled_color:要填充的颜色
Boundary_color:边界颜色
'''

def boundary_fill(x, y, filled_color, boundary_color):
    global im
    width = im.size[0]
    height = im.size[1]
    if 0 <= x < width and 0 <= y < height:
        if im.getpixel((x, y)) != filled_color and im.getpixel((x, y)) != boundary_color:
            im.putpixel((x, y), filled_color)
            boundary_fill(x + 1, y, filled_color, boundary_color)
            boundary_fill(x - 1, y, filled_color, boundary_color)
            boundary_fill(x, y + 1, filled_color, boundary_color)
            boundary_fill(x, y - 1, filled_color, boundary_color)
    return im


sys.setrecursionlimit(10000)
a = boundary_fill(61, 25, (0, 0, 255), (0, 0, 0))
a.show()
