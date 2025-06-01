# ----------------------------
# jcad v9.1
# by yoyomaji
# (c)2025. All rights reserved
# ----------------------------

# import libraries
import pygame
from colors import *
from refresh import *
from object import *

# init variables
pygame.init()
WIDHT, HEIGHT = 800, 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)

# main loop
Running = True
while Running:
  
  events = pygame.event.get()
  for event in events:
    if event.type == pygame.QUIT:
      pygame.quit
      quit
    if event.type == pygame.KEYDOWN:
      print('event keydown activeted')
    if event.type == pygame.KEYUP:
      print('event keyup activeted')
    if event.type == pygame.MOUSEMOTION:
      print('event mouse motion activeted')
    if event.type == pygame.MOUSEBUTTONDOWN:
      print('event mouse buytton down activeted')
  # 
  refresh_screen(SCREEN, bg_color, jpoints)
# formal wuit
pygame.quit()
quit()
