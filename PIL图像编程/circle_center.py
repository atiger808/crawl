# _*_ coding: utf-8 _*_
# @Time     : 2018/11/13 0:02
# @Author   : Ole211
# @Site     : 
# @File     : circle_center.py    
# @Software : PyCharm
from PIL import Image
import os
# os.chdir('d:/img')

def searchLeft(width, height, im):
    for w in range(width):
        for h in range(height):
            color = im.getpixel((w, h))
            if color != (255, 255, 255):
                return w

def searchRight(width, height, im):
    for w in range(width-1, -1, -1):
        for h in range(height):
            color = im.getpixel((w, h))
            if color != (255, 255, 255):
                return w

def searchBottom(width, height, im):
    for h in  range(height):
        for w in range(width):
            color = im.getpixel((w, h))
            if color != (255, 255, 255):
                return h

def searchTop(width, height, im):
    for h in range(height-1, -1, -1):
        for w in range(width):
            color = im.getpixel((w, h))
            if color != (255, 255, 255):
                return h
images = [f for f in os.listdir('d:/img') if f.endswith('.png')]
for f in images:
    f = 'd:/img/' + f
    im = Image.open(f)
    width, height = im.size #获取图像大小
    x0 = searchLeft(width, height, im)
    x1 = searchRight(width, height, im)
    y0 = searchTop(width, height, im)
    y1 = searchBottom(width, height, im)
    center = ((x0+x1)//2, (y0+y1)//2)

    im.putpixel(center, (255, 0, 0))
    im.save(f.split()[-2]+ '_center.png')
    # im.show()
    im.close()