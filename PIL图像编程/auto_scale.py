# _*_ coding: utf-8 _*_
# @Time     : 2018/11/13 14:52
# @Author   : Ole211
# @Site     : 
# @File     : auto_scale.py    
# @Software : PyCharm

from PIL import Image, ImageDraw, ImageFont
import os
os.chdir('d:/img')

def redraw(f, v1, v2):
    start = int(600*v1)
    end = int(600*v2)
    im = Image.open(f)

    for w in range(start):
        for h in range(36, 61):
            im.putpixel((w, h), (255, 0, 0))

    for w in range(start, end):
        for h in range(36, 61):
            im.putpixel((w, h), (0, 255, 0))

    for w in range(end, 600):
        for h in range(36, 61):
            im.putpixel((w, h), (255, 0, 255))

    draw = ImageDraw.Draw(im)
    font = ImageFont.truetype('ygyxsziti2.0.ttf',18)
    draw.text((start//2, 38), '第一行', (0, 0, 0), font=font)
    draw.text(((end-start)//2+start, 38), 'B', (0, 0, 0), font=font)
    draw.text(((600-end)//2+end, 38), 'C', (0, 0, 0), font=font)
    im.save(f)
    im.show()

if __name__ == '__main__':
    im = Image.new('RGBA', (600, 600), (255, 255, 255))
    im.save('test.png')
    redraw('test.png', 0.2, 0.6)