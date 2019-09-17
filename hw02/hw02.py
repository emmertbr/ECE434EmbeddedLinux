#!/usr/bin/env python3
#//////////////////////////////////////
# Blake Emmert 
# ECE 434 hw02: Etch-a-sketch w/ buttons and LEDs
# 9/17/19
# 
#//////////////////////////////////////
import curses
import argparse
import Adafruit_BBIO.GPIO as GPIO



def main(stdscr):
    #Get the size from the command line
    parser = argparse.ArgumentParser(description = 'Get size of box')
    parser.add_argument('--boxSize', type = int, default = 10)
    args = parser.parse_args()
    boxSize = args.boxSize
    
    #Clear and refresh the screen to ensure it is blank at the start
    stdscr.clear()
    stdscr.refresh()
    
    #Give the cursors color just for fun
    curses.start_color()
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_BLUE, curses.COLOR_BLACK)
    color = 1;
    
    #make initial box
    newBox(stdscr, boxSize, color)
    
    #Setup IO
    GPIO.setup("P9_11",GPIO.IN)
    GPIO.setup("P9_13",GPIO.IN)
    GPIO.setup("P9_19",GPIO.IN)
    GPIO.setup("P9_17",GPIO.IN)
    GPIO.setup("P9_21", GPIO.IN)
    GPIO.setup("P9_12",GPIO.OUT)
    GPIO.setup("P9_14",GPIO.OUT)
    GPIO.setup("P9_16",GPIO.OUT)
    GPIO.setup("P9_18",GPIO.OUT)
    
    #Set initial cursor position
    cursor_x = 0
    cursor_y = 0
    
    while True:
        #refreshes frame to get new position/printed X and checks for which key is pressed
        stdscr.refresh()
        
        #moves to new position based off of button press
        if GPIO.input("P9_11"):
            cursor_x = rightButton(cursor_x, boxSize)
        elif GPIO.input("P9_13"):
            cursor_y = upButton(cursor_y, boxSize)
        elif GPIO.input("P9_19"):
            cursor_y = downButton(cursor_y, boxSize)
        elif GPIO.input("P9_17"):
            cursor_x = leftButton(cursor_x, boxSize)
                
        #resets box if reset button is pressed
        elif GPIO.input("P9_21"):
            newBox(stdscr, boxSize, color)
            cursor_x = 0
            cursor_y = 0
            while GPIO.input("P9_21"):
                GPIO.output("P9_12", GPIO.HIGH)
                GPIO.output("P9_14", GPIO.HIGH)
                GPIO.output("P9_16", GPIO.HIGH)
                GPIO.output("P9_18", GPIO.HIGH)
            GPIO.output("P9_12", GPIO.LOW)
            GPIO.output("P9_14", GPIO.LOW)
            GPIO.output("P9_16", GPIO.LOW)
            GPIO.output("P9_18", GPIO.LOW)
            
        #outputs an X in the new position
        stdscr.addstr(cursor_y + 6, 2 + cursor_x, 'X', curses.color_pair(color))
        stdscr.move(6 + cursor_y, 2 + cursor_x)

#Function that handles a right button press
def rightButton(cursor_x, boxSize):
    if cursor_x < boxSize - 1:
        cursor_x = cursor_x + 1
        while GPIO.input("P9_11"):
            GPIO.output("P9_12", GPIO.HIGH)
        GPIO.output("P9_12", GPIO.LOW)
    return cursor_x

#Function that handles an up button press
def upButton(cursor_y, boxSize):
    if cursor_y > 0:
        cursor_y = cursor_y - 1
        while GPIO.input("P9_13"):
            GPIO.output("P9_14", GPIO.HIGH)
        GPIO.output("P9_14", GPIO.LOW)
    return cursor_y

#Function that handles a down button press
def downButton(cursor_y, boxSize):
    if cursor_y < boxSize - 1:
        cursor_y = cursor_y + 1
        while GPIO.input("P9_19"):
            GPIO.output("P9_16", GPIO.HIGH)
        GPIO.output("P9_16", GPIO.LOW)
    return cursor_y

#Function that handles a left button press
def leftButton(cursor_x, boxSize):
    if cursor_x > 0:
        cursor_x = cursor_x - 1
        while GPIO.input("P9_17"):
            GPIO.output("P9_18", GPIO.HIGH)
        GPIO.output("P9_18", GPIO.LOW)
    return cursor_x
        
def newBox(stdscr, boxSize, color):
    #Clear and refresh the window
    stdscr.clear()
    stdscr.refresh()
    
    #Title and instructions
    stdscr.addstr(0,0,"ETCH-A-SKETCH\nInstructions: Use the Up, Down, Left, and Right Buttons to move the cursor and draw.\n              To clear the drawing, press the reset button.\n              To exit the window, press Ctrl+c.")
    
    #Writes numbers for the boundary of the the etch a sketch work area
    j = 0;
    while j < boxSize:
        stdscr.addstr(5, 2 + j, str(j))
        stdscr.addstr(6 + j, 0, str(j))
        j = j + 1
    
    #Places initial X and moves cursor to starting positio
    stdscr.addstr(6, 2, 'X', curses.color_pair(color))
    stdscr.move(6, 2)
    stdscr.refresh()

curses.wrapper(main)