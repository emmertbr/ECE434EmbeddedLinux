#!/usr/bin/env python3
#//////////////////////////////////////
# Blake Emmert 
# ECE 434 hw01: Etch-a-sketch
# 9/12/19
# 
#//////////////////////////////////////
import Adafruit_BBIO.GPIO as GPIO
import time


GPIO.setup("P9_12",GPIO.OUT)

while True:
    GPIO.output("P9_12", GPIO.HIGH)
    time.sleep(0.005)
    GPIO.output("P9_12", GPIO.LOW)
    time.sleep(0.005)
        