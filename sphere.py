import curses
from typing import Text
import numpy as np
import math


brightness = ".:-=+*#%@"
s = 30

screen = curses.initscr()
w, h = screen.getmaxyx()
R = s
r = s/3

points=[]
for x in range(-w,w):
    for y in range(-h,h):
        for z in range(-w,w):
            if(round(((math.sqrt(x**2+y**2)-R)**2+z**2)/5)*5==round((r**2)/5)*5):
                points.append([x,y,z,"."])

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


    points.sort(key = lambda x: x[2])
    columns = []
    for point in points:
        if [round(point[0]*5)/5, round(point[1]*5)/5] not in columns:
            columns.append([round(point[0]*5)/5, round(point[1]*5)/5])
            point[3] = brightness[int(np.interp(-point[0], [-math.sqrt(3)*s, math.sqrt(3)*s], [2, len(brightness)-1]))]
        else:
            point[3] = brightness[int(np.interp(-point[0], [-math.sqrt(3)*s, math.sqrt(3)*s], [0, 1]))]
        

    for point in points:
        screen.addch(int(w/2 + w/3 / s * point[0]*np.interp(point[2], [-math.sqrt(3)*s, math.sqrt(3)*s], [0.5, 1])),
                     int(h/2 + h/3 / s * point[1]*np.interp(point[2], [-math.sqrt(3)*s, math.sqrt(3)*s], [0.5, 1])), point[3])

    key = screen.getch()
    if key == curses.KEY_RIGHT:
        for i in range(len(points)):
            points[i][0],points[i][1],points[i][2] = [[sum(a*b for a, b in zip(X_row, Y_col))
                          for Y_col in zip(*Rx)] for X_row in [points[i]]][0]
    elif key == curses.KEY_UP:
        for i in range(len(points)):
            points[i][0],points[i][1],points[i][2] = [[sum(a*b for a, b in zip(X_row, Y_col))
                          for Y_col in zip(*Ry)] for X_row in [points[i]]][0]
    elif key == curses.KEY_LEFT:
        for i in range(len(points)):
            points[i][0],points[i][1],points[i][2] = [[sum(a*b for a, b in zip(X_row, Y_col))
                          for Y_col in zip(*rx)] for X_row in [points[i]]][0]
    elif key == curses.KEY_DOWN:
        for i in range(len(points)):
            points[i][0],points[i][1],points[i][2] = [[sum(a*b for a, b in zip(X_row, Y_col))
                          for Y_col in zip(*ry)] for X_row in [points[i]]][0]
