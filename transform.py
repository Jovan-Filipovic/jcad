# import libraries
import numpy as np
import pygame

# define functions
def screen_refresh(surface, bg_color, fg_color, jpoints, jobjects):
  surface.fill (bg_color)
  for i in range (0, len(jpoints), 1):
    xw = jpoints[i][0]
    yw = jpoints[i][1]
    zw = jpoints[i][2]
    print(xw, yw, zw)
