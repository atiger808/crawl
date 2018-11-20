# _*_ coding: utf-8 _*_
# @Time     : 2018/11/12 22:56
# @Author   : Ole211
# @Site     : 
# @File     : image_open.py    
# @Software : PyCharm

from PIL import Image
import os
os.chdir('d:/img')
#
im = Image.open('lena.jpg')
print(im.size)
# print(im.histogram())
# print(im.getpixel((100, 200)))
# im1 = Image.new('RGBA', (800, 500), (255,255, 255))
# from random import randint
# for w in range(200, 280):
#     for h in range(100, 200):
#         r = randint(0, 255)
#         g = randint(0, 255)
#         b = randint(0, 255)
#         im1.putpixel((w, h), (r, g, b))
# # im1.show()
# for w in range(200, 280):
#     for h in range(100, 200):
#         color = im1.getpixel((w, h))
#         im1.putpixel((w+200, h), color)
# # im1.show()
# im.save('r.bmp')
# # 图像缩放
# im2 = im1.resize((100, 100))
# # 图像旋转
# # 逆时针旋转图像， rotate方法支持任意角度的旋转，
# # 而transpose方法支持部分特殊角度的旋转， 如90, 180
# # 270,以及水平，垂直翻转
# im2 = im2.rotate(32, expand=True)
# im2.show()
# im3 = im1.transpose(Image.ROTATE_90)
# im3.show()
# im4 = im1.transpose(Image.FLIP_LEFT_RIGHT)
# im4.show()
# # 图像的裁剪与粘贴
# box = (120, 194, 220, 294)
# region = im.crop(box)
# # region = region.transpose(Image.ROTATE_180)
# region = region.rotate(180, expand=True)
# im.paste(region, box)
# im.show()

from  PIL import ImageFilter
# 图像分离，r, g, b分离
# 图像增强
im_gray = im.convert('L')
r, g, b = im.split()
im5 = im.filter(ImageFilter.DETAIL)
im5.show()
# 图像模糊
im6 = im.filter(ImageFilter.BLUR)
im6.show()
# 图像边缘提取
im7 = im_gray.filter(ImageFilter.FIND_EDGES)
im7.show()

# 图像的点运算， 整体变暗， 变亮
im8 = im.point(lambda i: i*1.3)
im9 = im.point(lambda i : i*0.7)
im8.show()
im9.show()


im  = Image.open('lena.jpg')
# 图像增强模块
from PIL import ImageEnhance
enh = ImageEnhance.Brightness(im)
enh.enhance(1.3).show()

# 图像对比度增强
from PIL import ImageEnhance
enh = ImageEnhance.Contrast(im)
enh.enhance(1.3).show()

# 冷暖色调调整
r, g, b = im.split()
r = r.point(lambda i:i*1.3)
g = g.point(lambda i:i*0.9)
b = b.point(lambda i:0)
im10 = Image.merge(im.mode, (r, g, b))
im10.show()
