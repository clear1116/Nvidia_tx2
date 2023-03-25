#coding=UTF-8
import Jetson.GPIO as GPIO
import time  # 引用需要用的库
LED_Pin = 40
GPIO.setmode(GPIO.BOARD)
GPIO.setup(LED_Pin, GPIO.OUT)  # 设置要操作的引脚,并将引脚设置为输出引脚
while True:
    GPIO.output(LED_Pin, GPIO.HIGH)
    time.sleep(1)
    GPIO.output(LED_Pin, GPIO.LOW)
    time.sleep(1)  # 通过切换GPIO的电平来点亮和熄灭LED
GPIO.cleanup()  # 最后在退出循环的时候清除GPIO的状态
