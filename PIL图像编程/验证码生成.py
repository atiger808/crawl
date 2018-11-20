# _*_ coding: utf-8 _*_
# @Time     : 2018/11/13 15:25
# @Author   : Ole211
# @Site     : 
# @File     : 验证码生成.py    
# @Software : PyCharm

from random import choice, randint, randrange
import string
from PIL import Image, ImageDraw, ImageFont

# 验证码候选字符集
characters = string.ascii_letters + string.digits
print(characters)

box = Image.new('RGBA', (20, 60), (255, 255, 255))

def selectedCharacters(length):
    '''返回length个随机字符的字符串'''
    result = ''.join(choice(characters) for _ in range(length))
    return result

def getColor():
    '''返回随机颜色'''
    r = randint(0, 255)
    g = randint(0, 255)
    b = randint(0, 255)
    return (r, g, b)

def main(size=(200, 100), characterNumber=4, bgcolor=(255, 255, 255)):
    # 创建空白区域和绘图对象
    imageTemp= Image.new('RGB', size, bgcolor)
    draw = ImageDraw.Draw(imageTemp)

    # 生成并计算随机字符串的宽度和高度
    text = selectedCharacters(characterNumber)
    font = ImageFont.truetype('ygyxsziti2.0.ttf', 48)
    w, h = draw.textsize(text, font)
    if w + 2*characterNumber>size[0] or h>size[1]:
        print('尺寸不合法')
        return
    # 绘制随机字符串中的字符
    startX = 0
    widthEachCharacter = w//characterNumber
    for i in range(characterNumber):
        startX += widthEachCharacter + 1
        # 每一个字符在图片的y坐标随机计算
        position = (startX, (size[1] - h)//2 + randint(-10, 10))
        draw.text(xy=position, text=text[i], font=font, fill=getColor())

    # 对像素位置进行微调， 实现扭曲额效果
    imageFinal = Image.new('RGB', size, bgcolor)
    pixelsFinal = imageFinal.load()
    pixelsTemp = imageTemp.load()
    for y in range(size[1]):
        offset = randint(-1, 0)
        for x in range(size[0]):
            newx = x + offset
            if newx >= size[0]:
                newx = size[0] -1
            elif newx < 0:
                newx = 0
            pixelsFinal[newx, y] = pixelsTemp[x, y]

    # 绘制随机颜色随机位置的干扰像素
    draw = ImageDraw.Draw(imageFinal)
    for i in range(int(size[0]*size[1]*0.07)):
        draw.point((randrange(0, size[0]), randrange(0, size[1])), fill=getColor())

    # 绘制8条干扰直线
    for i in range(8):
        start = (0, randrange(size[1]))
        end = (size[0], randrange(size[1]))
        draw.line([start, end], fill=getColor(), width=1)

     # 绘制8条随机弧线
    for i in range(8):
        start = (-50, -50)
        end = (size[0]+10, randint(0, size[1]+10))
        draw.arc(start+end, 0, 360, fill=getColor())

    # 保存并显示图片
    imageFinal.save('code.jpg')
    print(text)
    imageFinal.show()

if __name__ == '__main__':
    main((200, 100), 5, (255, 255, 255))