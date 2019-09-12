#!/usr/bin/env python3
#//////////////////////////////////////
# Blake Emmert 
# ECE 434 hw01: Etch-a-sketch
# 9/12/19
# 
#//////////////////////////////////////
import curses
import argparse

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
    
    #Set initial cursor position
    cursor_x = 0
    cursor_y = 0
    
    
    
    
    
    
    while True:
        #refreshes frame to get new position/printed X and checks for which key is pressed
        stdscr.refresh()
        pressedKey = stdscr.getch()
        
        #moves to new position based off of key press
        if pressedKey == curses.KEY_UP:
            if cursor_y > 0:
                cursor_y = cursor_y - 1
        elif pressedKey == curses.KEY_DOWN:
            if cursor_y < boxSize - 1:
                cursor_y = cursor_y + 1
        elif pressedKey == curses.KEY_LEFT:
            if cursor_x > 0:
                cursor_x = cursor_x - 1;
        elif pressedKey == curses.KEY_RIGHT:
            if cursor_x < boxSize - 1:
                cursor_x = cursor_x + 1
                
        #resets box if n is pressed
        elif pressedKey == ord('n'):
            color = 1
            newBox(stdscr, boxSize, color)
            cursor_x = 0
            cursor_y = 0
        
        #changes color if c is pressed
        elif pressedKey == ord('c'):
            if color == 1:
                color = 2
            else:
                color = 1
            
        #outputs an X in the new position
        stdscr.addstr(cursor_y + 6, 2 + cursor_x, 'X', curses.color_pair(color))
        stdscr.move(6 + cursor_y, 2 + cursor_x)
        
        
def newBox(stdscr, boxSize, color):
    #Clear and refresh the window
    stdscr.clear()
    stdscr.refresh()
    
    #Title and instructions
    stdscr.addstr(0,0,"ETCH-A-SKETCH\nInstructions: Use the Up, Down, Left, and Right arrow keys to move the cursor and draw.\n              To change the color of the cursor press 'c'.\n              To clear the drawing, press 'n'.")
    
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