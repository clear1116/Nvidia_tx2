from periphery import SPI
import Jetson.GPIO as GPIO
import time
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import numpy as np


DC_Pin = 11
CS_Pin = 12
RES_Pin = 40
GPIO.setmode(GPIO.BOARD)
GPIO.setup(CS_Pin, GPIO.OUT)
GPIO.setup(DC_Pin, GPIO.OUT)
GPIO.setup(RES_Pin, GPIO.OUT)
spi = SPI("/dev/spidev3.1", 3, 10000000)


def OLED_Write_CMD(CMD):
	GPIO.output(CS_Pin, GPIO.LOW)  # 拉低CS
	GPIO.output(DC_Pin, GPIO.LOW)  # 写命令拉低
	spi.transfer(CMD)
	GPIO.output(CS_Pin, GPIO.HIGH)  # 写完拉高CS



def OLED_Write_DATA(DATA):
	GPIO.output(CS_Pin, GPIO.LOW)  # 拉低CS
	GPIO.output(DC_Pin, GPIO.HIGH)  # 写数据拉高
	spi.transfer(DATA)
	GPIO.output(CS_Pin, GPIO.HIGH)  # 写完拉高CS



def OLED_Init():

	#GPIO.output(CS_Pin, GPIO.LOW)
	GPIO.output(RES_Pin, GPIO.LOW)
	time.sleep(0.1)
	GPIO.output(RES_Pin, GPIO.HIGH)
	time.sleep(0.1)

	OLED_Write_CMD([0xAE])  # --关闭屏幕
	OLED_Write_CMD([0xD5, 0x80])  # --设置分频/振荡器频率
	OLED_Write_CMD([0xA8, 0x3F])  # --设置多路传输比率
	OLED_Write_CMD([0x20, 0x02])  # -Set 设置寻址模式 设置为页寻址 (0x00/0x01/0x02)
	OLED_Write_CMD([0xDA, 0x12])  # --设置列引脚硬件配置
	OLED_Write_CMD([0xA1, 0xC8])  # --0xa0左右反置 0xa1正常  0xc0上下反置 0xc8正常
	OLED_Write_CMD([0x40])  # --设置屏幕（GDDRAM）起始行 (0x40~0x7F)0x7F-0x40=63
	OLED_Write_CMD([0xD3, 0x00])  # -设置偏移 偏移为0 (0x00~0x3F)
	OLED_Write_CMD([0x81, 0xCF])  # --设置对比度 (0x00~0xFF)
	OLED_Write_CMD([0xD9, 0xF1])  # --设置充电时间 15周期充电,1周期放电
	OLED_Write_CMD([0xDB, 0x40])  # --调整VCOMH调节器的输出(0x00/0x20/0x30/0x40)
	OLED_Write_CMD([0x8D, 0x14])  # --设置电荷泵使能 enable/disable(0x14/0x10)
	OLED_Write_CMD([0x00, 0x10])  # ---设置列地址

	OLED_Write_CMD([0xA4])  # 黑屏/亮屏 0xA4 根据RAM 内容显示 / 0xA5 每个oled都点亮 全部显示
	OLED_Write_CMD([0xA6])  # 正显反显 (0xa6/0xa7)
	OLED_Write_CMD([0xAF])  # 打开屏幕


def OLED_Clear():
	buf = [0x00] * 128
	for i in range(8):
		OLED_Write_CMD([0xB0 | i])  # --设置页
		OLED_Write_CMD([0x00, 0x10])  # --列地址低4位/高4位
		OLED_Write_DATA(buf)


def OLED_FILL():
	buf = [0xFF] * 128
	for i in range(8):
		OLED_Write_CMD([0xB0 | i])  # --设置页
		OLED_Write_CMD([0x00])
		OLED_Write_CMD([0x10]) # --列地址低4位/高4位
		OLED_Write_DATA(buf)


def OLED_Show(img):
	for i in range(8):
		buf = img[128*i:128*(i+1)]
		OLED_Write_CMD([0xB0 | i])  # --设置页
		OLED_Write_CMD([0x00, 0x10])  # --列地址低4位/高4位
		OLED_Write_DATA(buf)

def OLED_Show_text(text:str):
	width = 128
	height = 64
	# Create an image object and draw the image you want to display
	image = Image.new('1', (width, height))
	draw = ImageDraw.Draw(image)
	draw.rectangle((0, 0, width, height), outline=0, fill=0)
	font = ImageFont.truetype('/usr/share/fonts/MSYH/msyh.ttc',size=16)
	draw.text((0, 0), text, font=font, fill=255)
	ssd1306_data = img_to_ssd1306(np.array(image))
	OLED_Show(ssd1306_data)

def OLED_Show_img(path:str):
	image = Image.open(path)
	image = image.resize((128, 64)).convert('1')
	ssd1306_data = img_to_ssd1306(np.array(image))
	OLED_Show(ssd1306_data)

def img_to_ssd1306(np_image):
	bits = np.packbits(np.array(np_image),axis=0,bitorder='little')# create a byte array for the SSD1306 data
	ssd1306_data = bits.reshape(-1).tolist()
	return ssd1306_data

OLED_Init()
# fps = 0
# for i in range(500):
# 	t0=time.time()
# 	OLED_Show_text(f"FPS={int(fps)}")
# 	t1=time.time()
# 	fps = 1/(t1-t0)
# 	time.sleep(0.3)
OLED_Show_img('R-C.jpg')
time.sleep(10)
OLED_Show_text('给初遥的小心心')
time.sleep(10)
OLED_Clear()