import curses
from typing import Text
import numpy as np
import math

text = """
                 !#########       #                
               !########!          ##!               
            !########!               ###             
         !##########                  ####           
       ######### #####                ######         
        !###!      !####!              ######        
          !           #####            ######!       
                        !####!         #######      
                           #####       #######       
                             !####!   #######!       
                                ####!########        
             ##                   ##########         
           ,######!          !#############          
         ,#### ########################!####!        
       ,####'     ##################!'    #####      
     ,####'            #######              !####!   
    ####'                                      ##### 
    ~##                                          ##~ """

brightness = ".:-=+*#%@"
s = 30
#points = [[2*s*(x-0.5), 2*s*(y-0.5), 2*s*(z-0.5)]
#          for x in range(2) for y in range(2) for z in range(2)]

#points += [[x, -s, -s] for x in range(-s, s+1)]
#points += [[x, s, -s] for x in range(-s, s+1)]
#points += [[s, x, -s] for x in range(-s, s+1)]
#points += [[-s, -x, -s] for x in range(-s, s+1)]

#points += [[s, s, x] for x in range(-s, s+1)]
#points += [[s, -s, x] for x in range(-s, s+1)]
#points += [[-s, s, x] for x in range(-s, s+1)]
#points += [[-s, -s, x] for x in range(-s, s+1)]

#points += [[-s, x, s] for x in range(-s, s+1)]
#points += [[s, x, s] for x in range(-s, s+1)]
#points += [[x, s, s] for x in range(-s, s+1)]
#points += [[x, -s, s] for x in range(-s, s+1)]
screen = curses.initscr()
w, h = screen.getmaxyx()
curses.start_color()
curses.init_pair(1,curses.COLOR_YELLOW, curses.COLOR_RED)
curses.init_pair(2,curses.COLOR_YELLOW, curses.COLOR_YELLOW)

text = text.splitlines()
 
points=[]
for i, line in enumerate(text):
    for j, char in enumerate(line):

        if char != " ":
            points.append([2 * s * (i - len(text)/2)/len(text),
                          2 * s*(j - len(line)/2)/len(line), 0])
            points.append([2 * s * (i - len(text)/2)/len(text),
                          2 * s*(j - len(line)/2)/len(line), -1])
            points.append([2 * s * (i - len(text)/2)/len(text),
                          2 * s*(j - len(line)/2)/len(line), 1])
            points.append([2 * s * (i - len(text)/2)/len(text),
                          2 * s*(j - len(line)/2)/len(line), -2])
            points.append([2 * s * (i - len(text)/2)/len(text),
                          2 * s*(j - len(line)/2)/len(line), 2])

curses.curs_set(0)
curses.noecho()
curses.cbreak()
screen.keypad(True)
screen.clear()
height, width = screen.getmaxyx()
theta = math.pi/72

Rx = [[1.0, 0.0, 0.0],
      [0.0, math.cos(theta), -math.sin(theta)],
      [0.0, math.sin(theta), math.cos(theta)]]

Ry = [[math.cos(theta), 0,  math.sin(theta)],
      [0, 1, 0],
      [-math.sin(theta), 0, math.cos(theta)]]

rx = [[1.0, 0.0, 0.0],
      [0.0, math.cos(-theta), -math.sin(-theta)],
      [0.0, math.sin(-theta), math.cos(-theta)]]

ry = [[math.cos(-theta), 0,  math.sin(-theta)],
      [0, 1, 0],
      [-math.sin(-theta), 0, math.cos(-theta)]]

while True:
    screen.refresh()
    screen.clear()
    curses.napms(30)
    screen.bkgd(' ',curses.color_pair(1))
    for point in points:
        screen.addch(int(w/2 + w/2 / s * point[0]*np.interp(point[2], [-math.sqrt(3)*s, math.sqrt(3)*s], [0.5, 1])),
                     int(h/2 + h/2 / s * point[1]*np.interp(point[2], [-math.sqrt(3)*s, math.sqrt(3)*s], [0.5, 1])), brightness[int(np.interp(point[2], [-math.sqrt(3)*s, math.sqrt(3)*s], [0, len(brightness)-1]))],curses.color_pair(2))

    key = screen.getch()
    if key == curses.KEY_RIGHT:
        for i in range(len(points)):
            points[i] = [[sum(a*b for a, b in zip(X_row, Y_col))
                          for Y_col in zip(*Rx)] for X_row in [points[i]]][0]
    elif key == curses.KEY_UP:
        for i in range(len(points)):
            points[i] = [[sum(a*b for a, b in zip(X_row, Y_col))
                          for Y_col in zip(*Ry)] for X_row in [points[i]]][0]
    elif key == curses.KEY_LEFT:
        for i in range(len(points)):
            points[i] = [[sum(a*b for a, b in zip(X_row, Y_col))
                          for Y_col in zip(*rx)] for X_row in [points[i]]][0]
    elif key == curses.KEY_DOWN:
        for i in range(len(points)):
            points[i] = [[sum(a*b for a, b in zip(X_row, Y_col))
                          for Y_col in zip(*ry)] for X_row in [points[i]]][0]
