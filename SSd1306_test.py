#import Adafruit_SSD1306
import time
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import cv2
import numpy as np

#OLED = Adafruit_SSD1306.SSD1306_128_64(rst=None, spi=4)  # 注意 使用的是哪组i2c的接口，对应调整i2c_bus取值

# OLED.begin()  # 初始化屏幕并清屏
# OLED.clear()
# OLED.display()
time.sleep(1)

font = ImageFont.load_default()  # 设置字体为默认字体

width = 128  # 设置屏幕长宽，并创建画布
height = 64
image = Image.new("1", (width, height))
Draw = ImageDraw.Draw(image)  # 设置刷新区域，并写入字符串，这里调用的是PIL图形库的画图函数
Draw.rectangle((0, 0, width, height), outline=0, fill=0)
Draw.text((0, 0), "oled Testing", font=font, fill=255)
cc=np.array(image)
cv2.imshow(cc)
cv2.waitKey(0)
print(type(image))
