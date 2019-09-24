#!/usr/bin/env python3
# EtchASketch program on 8x8Matrix using buttons
#Blake Emmert
#hw03
#9/24/19
# sudo apt install python3-smbus

import smbus
import time
import subprocess
import Adafruit_BBIO.GPIO as GPIO
import math


#Sets up button and LED GPIO pins
GPIO.setup("P9_11",GPIO.IN)
GPIO.setup("P9_13",GPIO.IN)
GPIO.setup("P9_19",GPIO.IN)
GPIO.setup("P9_17",GPIO.IN)
GPIO.setup("P9_23", GPIO.IN)
GPIO.setup("P9_12",GPIO.OUT)
GPIO.setup("P9_14",GPIO.OUT)
GPIO.setup("P9_16",GPIO.OUT)
GPIO.setup("P9_18",GPIO.OUT)

bus = smbus.SMBus(2)
matrix = 0x70

bus.write_byte_data(matrix, 0x21, 0)   # Start oscillator (p10)
bus.write_byte_data(matrix, 0x81, 0)   # Disp on, blink off (p11)
bus.write_byte_data(matrix, 0xe7, 0)   # Full brightness (page 15)

#Initializes matrix LED starting points and list that keeps track of
#which LEDs are currently lit. 
empty = [0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00
]

LEDs = [0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00
]

LitLEDs = []

newList = [True, False, False, False, False, False, False, False]
LitLEDs.append(newList)

#Fills List with False to indicate no LEDs are lit
for i in range(7):
    newList = []
    for j in range(8):
        newList.append(False)
    LitLEDs.append(newList)

bus.write_i2c_block_data(matrix, 0, empty)

#function that handles button presses and updating the matrix
def main(LEDs, LitLEDs):
    cursor_x = 0
    cursor_y = 0
    
    while True:
            changed = False
            
            #moves to new position based off of button press
            if GPIO.input("P9_11"):
                temp = cursor_x
                cursor_x = rightButton(cursor_x)
                if(cursor_x != temp):
                    changed = True
            elif GPIO.input("P9_13"):
                temp = cursor_y
                cursor_y = upButton(cursor_y)
                if(cursor_y != temp):
                    changed = True
            elif GPIO.input("P9_19"):
                temp = cursor_y
                cursor_y = downButton(cursor_y)
                if(cursor_y != temp):
                    changed = True
            elif GPIO.input("P9_17"):
                temp = cursor_x
                cursor_x = leftButton(cursor_x)
                if(cursor_x != temp):
                    changed = True
                    
            #resets box if reset button is pressed
            elif GPIO.input("P9_23"):
                while GPIO.input("P9_23"):
                    GPIO.output("P9_12", GPIO.HIGH)
                    GPIO.output("P9_14", GPIO.HIGH)
                    GPIO.output("P9_16", GPIO.HIGH)
                    GPIO.output("P9_18", GPIO.HIGH)
                GPIO.output("P9_12", GPIO.LOW)
                GPIO.output("P9_14", GPIO.LOW)
                GPIO.output("P9_16", GPIO.LOW)
                GPIO.output("P9_18", GPIO.LOW)
                newScreen(empty)
            
	    #makes sure an LED isn't already lit and if not updates the matrix and list
	    #tracking which LEDs are lit.
            if(changed):
                index = 2*cursor_x;
                ledValue = int(math.pow(2,cursor_y))
                if(LitLEDs[cursor_x][cursor_y] == False):
                    LEDs[index] = LEDs[index] + ledValue
                    LitLEDs[cursor_x][cursor_y] = True;
                bus.write_i2c_block_data(matrix, 0, LEDs)

#Function that handles a right button press
def rightButton(cursor_x):
    if cursor_x < 8 - 1:
        cursor_x = cursor_x + 1
        while GPIO.input("P9_11"):
            GPIO.output("P9_12", GPIO.HIGH)
        GPIO.output("P9_12", GPIO.LOW)
    return cursor_x

#Function that handles an up button press
def upButton(cursor_y):
    if cursor_y < 8 - 1:
        cursor_y = cursor_y + 1
        while GPIO.input("P9_13"):
            GPIO.output("P9_14", GPIO.HIGH)
        GPIO.output("P9_14", GPIO.LOW)
    return cursor_y

#Function that handles a down button press
def downButton(cursor_y):
    if cursor_y > 0:
        cursor_y = cursor_y - 1
        while GPIO.input("P9_19"):
            GPIO.output("P9_16", GPIO.HIGH)
        GPIO.output("P9_16", GPIO.LOW)
    return cursor_y
    
    

#Function that handles a left button press
def leftButton(cursor_x):
    if cursor_x > 0:
        cursor_x = cursor_x - 1
        while GPIO.input("P9_17"):
            GPIO.output("P9_18", GPIO.HIGH)
        GPIO.output("P9_18", GPIO.LOW)
    return cursor_x

#Function that resets the matrix
def newScreen(empty):
    bus.write_i2c_block_data(matrix, 0, empty)
    
    LEDs = [0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00
    ]
    
    LitLEDs = []

    newList = [True, False, False, False, False, False, False, False]
    LitLEDs.append(newList)

    for i in range(7):
        newList = []
        for j in range(8):
            newList.append(False)
        LitLEDs.append(newList)
    main(LEDs, LitLEDs)
main(LEDs, LitLEDs)
