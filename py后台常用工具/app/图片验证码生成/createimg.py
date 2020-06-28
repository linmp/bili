import random
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
from .config import width, height
import os.path

dirs = os.path.dirname(__file__)

# 随机背景颜色
def getRandomColor():
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)
    return (r, g, b)

# 随机字符串
def getRandomChar():
    random_num = str(random.randint(0, 9))
    random_lower = chr(random.randint(97, 122))  # 小写字母a~z
    random_upper = chr(random.randint(65, 90))  # 大写字母A~Z
    random_char = random.choice([random_num, random_lower, random_upper])
    return random_char

# 干扰线
def drawLine(draw):
    for i in range(5):
        x1 = random.randint(0, width)
        x2 = random.randint(0, width)
        y1 = random.randint(0, height)
        y2 = random.randint(0, height)
        draw.line((x1, y1, x2, y2), fill=getRandomColor())

# 干扰点
def drawPoint(draw):
    for i in range(50):
        x = random.randint(0, width)
        y = random.randint(0, height)
        draw.point((x, y), fill=getRandomColor())

# 制图
def createImg():
    """
    创建验证码的方法，封装好了方法，只需要调用就OK
    # image_data, text = createimg.createImg()
    # resp = make_response(image_data)
    # resp.headers["Content-Type"] = "image/jpg"
    # return resp
    :return: (image_data, text) 分别是图片的资源，图片的字符串小写
    """
    bg_color = getRandomColor()
    # 创建一张随机背景色的图片
    img = Image.new(mode="RGB", size=(width, height), color=bg_color)
    # 获取图片画笔，用于描绘字
    draw = ImageDraw.Draw(img)
    # 修改字体
    font = ImageFont.truetype(font=dirs+"/fonts/Arial.ttf", size=36)

    str_of_code = ''
    for i in range(5):
        # 随机生成5种字符+5种颜色
        random_txt = getRandomChar()
        txt_color = getRandomColor()
        # 避免文字颜色和背景色一致重合
        while txt_color == bg_color:
            txt_color = getRandomColor()
        # 根据坐标填充文字
        draw.text((10 + 30 * i, 3), text=random_txt, fill=txt_color, font=font)
        # 添加文字进入字符串
        str_of_code += random_txt

        # 画干扰线点
    drawLine(draw)
    drawPoint(draw)

    buf = BytesIO()
    img.save(buf, 'jpeg')
    buf_str = buf.getvalue()
    return (buf_str, str_of_code.lower())
