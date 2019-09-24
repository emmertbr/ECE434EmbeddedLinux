#!/usr/bin/env python3
#Encoder EtchASketch
#Blake Emmert
#hw03
#9/24/19

from Adafruit_BBIO.Encoder import RotaryEncoder, eQEP1
from Adafruit_BBIO.Encoder import RotaryEncoder, eQEP2
import time
import smbus
import subprocess
import math
import Adafruit_BBIO.GPIO as GPIO

# Instantiate the class to access channel eQEP1 and eQEP2, and initialize
# that channel

myEncoder1 = RotaryEncoder(eQEP1)
myEncoder1.setAbsolute()
myEncoder1.enable()
myEncoder2 = RotaryEncoder(eQEP2)
myEncoder2.setAbsolute()
myEncoder2.enable()


encoder_x = 0;
encoder_y = 0;

GPIO.setup("P9_23", GPIO.IN)

bus = smbus.SMBus(2)
matrix = 0x70

bus.write_byte_data(matrix, 0x21, 0)   # Start oscillator (p10)
bus.write_byte_data(matrix, 0x81, 0)   # Disp on, blink off (p11)
bus.write_byte_data(matrix, 0xe7, 0)   # Full brightness (page 15)

#initialize matrix starting point and lists to track which LEDs are lit
empty = [0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00
]

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

bus.write_i2c_block_data(matrix, 0, empty)

#Function that handles reading the encoders and updating the matrix
def main(LEDs, LitLEDs, encoder_x, encoder_y):
    cursor_x = 0
    cursor_y = 0
    
    while True:
            changed = False
            
            #moves to new position based off of the encoder moves
            if myEncoder1.position > encoder_x+3:
                temp = cursor_x
                cursor_x = rightButton(cursor_x)
                if(cursor_x != temp):
                    changed = True
                encoder_x = myEncoder1.position
            elif myEncoder2.position > encoder_y+3:
                temp = cursor_y
                cursor_y = upButton(cursor_y)
                if(cursor_y != temp):
                    changed = True
                encoder_y = myEncoder2.position
            elif myEncoder2.position < encoder_y-3:
                temp = cursor_y
                cursor_y = downButton(cursor_y)
                if(cursor_y != temp):
                    changed = True
                encoder_y = myEncoder2.position
            elif myEncoder1.position < encoder_x-3:
                temp = cursor_x
                cursor_x = leftButton(cursor_x)
                if(cursor_x != temp):
                    changed = True
                encoder_x = myEncoder1.position
                    
            #resets box if reset button is pressed
            elif GPIO.input("P9_23"):
                newScreen(empty, encoder_x, encoder_y)
            
	    #Checks that the LED is not already lit and if not
	    #updates the matrix and list of lit LEDs
            if(changed):
                index = 2*cursor_x;
                ledValue = int(math.pow(2,cursor_y))
                if(LitLEDs[cursor_x][cursor_y] == False):
                    LEDs[index] = LEDs[index] + ledValue
                    LitLEDs[cursor_x][cursor_y] = True;
                bus.write_i2c_block_data(matrix, 0, LEDs)

#Function that handles encoder movement indicating a right movement
def rightButton(cursor_x):
    if cursor_x < 8 - 1:
        cursor_x = cursor_x + 1
    return cursor_x

#Function that handles encoder movement indicating up movement
def upButton(cursor_y):
    if cursor_y < 8 - 1:
        cursor_y = cursor_y + 1
    return cursor_y

#Function that handles a encoder movement indicating down movement
def downButton(cursor_y):
    if cursor_y > 0:
        cursor_y = cursor_y - 1
    return cursor_y
    
    

#Function that handles encoder movement indicating left movement
def leftButton(cursor_x):
    if cursor_x > 0:
        cursor_x = cursor_x - 1
    return cursor_x

#Function that resets the matrix and LED lists
def newScreen(empty, encoder_x, encoder_y):
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
    main(LEDs, LitLEDs, encoder_x, encoder_y)
main(LEDs, LitLEDs, encoder_x, encoder_y)
