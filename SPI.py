from periphery import SPI
import Jetson.GPIO as GPIO

DC_Pin = 11
CS_Pin = 12
GPIO.setmode(GPIO.BOARD)
GPIO.setup(CS_Pin, GPIO.OUT)
GPIO.setup(DC_Pin, GPIO.OUT)
spi = SPI("/dev/spidev3.0", 0, 1000000)


def OLED_Write_CMD(CMD:bytes):
    GPIO.output(CS_Pin, GPIO.LOW)   # 拉低CS
    GPIO.output(DC_Pin, GPIO.LOW)   # 写命令拉低
    data_in = spi.transfer(CMD)
    GPIO.output(CS_Pin, GPIO.HIGH)  # 写完拉高CS
    return data_in


def OLED_Write_DATA(DATA):
    GPIO.output(CS_Pin, GPIO.LOW)   # 拉低CS
    GPIO.output(DC_Pin, GPIO.HIGH)   # 写数据拉高
    data_in = spi.transfer(DATA)
    GPIO.output(CS_Pin, GPIO.HIGH)  # 写完拉高CS
    return data_in

def OLED_Init():
	
	OLED_Write_CMD(0xAE) #--turn off oled panel
	OLED_Write_CMD(0x00) #---set low column address
	OLED_Write_CMD(0x10) #---set high column address
	OLED_Write_CMD(0x40) #--set start line address  Set Mapping RAM Display Start Line (0x00~0x3F)
	OLED_Write_CMD(0x81) #--set contrast control register
	OLED_Write_CMD(0xCF) # Set SEG Output Current Brightness
	OLED_Write_CMD(0xA1) #--Set SEG/Column Mapping     0xa0左右反置 0xa1正常
	OLED_Write_CMD(0xC8) #Set COM/Row Scan Direction   0xc0上下反置 0xc8正常
	OLED_Write_CMD(0xA6) #--set normal display
	OLED_Write_CMD(0xA8) #--set multiplex ratio(1 to 64)
	OLED_Write_CMD(0x3f) #--1/64 duty
	OLED_Write_CMD(0xD3) #-set display offset	Shift Mapping RAM Counter (0x00~0x3F)
	OLED_Write_CMD(0x00) #-not offset
	OLED_Write_CMD(0xd5) #--set display clock divide ratio/oscillator frequency
	OLED_Write_CMD(0x80) #--set divide ratio, Set Clock as 100 Frames/Sec
	OLED_Write_CMD(0xD9) #--set pre-charge period
	OLED_Write_CMD(0xF1) #Set Pre-Charge as 15 Clocks & Discharge as 1 Clock
	OLED_Write_CMD(0xDA) #--set com pins hardware configuration
	OLED_Write_CMD(0x12)
	OLED_Write_CMD(0xDB) #--set vcomh
	OLED_Write_CMD(0x40) #Set VCOM Deselect Level
	OLED_Write_CMD(0x20) #-Set Page Addressing Mode (0x00/0x01/0x02)
	OLED_Write_CMD(0x02) #
	OLED_Write_CMD(0x8D) #--set Charge Pump enable/disable
	OLED_Write_CMD(0x14) #--set(0x10) disable
	OLED_Write_CMD(0xA4) # Disable Entire Display On (0xa4/0xa5)
	OLED_Write_CMD(0xA6) # Disable Inverse Display On (0xa6/a7)
	OLED_Write_CMD(0xAF)

def OLED_Clear():
	buf = [0x00] * 128
	for i in range(8):
		OLED_Write_CMD(0xB0 | i)
		OLED_Write_CMD(0x00)
		OLED_Write_CMD(0x10)
		OLED_Write_DATA(buf)
def OLED_Clear():
