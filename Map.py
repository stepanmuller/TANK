from tkinter import *
from random import randint
import sys
import os
import tkinter as tk
from playsound import playsound
from PIL import ImageTk
from PIL import Image
from math import *
import pyautogui
import pygame
from Artillery import Artillery
from Json_arbeiter import Arbeiter
from Minimap import Minimap

class Map:  
  def __init__(self, canvas, window, period, screen_width, screen_height):
    self.canvas = canvas
    self.window = window
    self.period = period
    self.screen_width = screen_width
    self.screen_height = screen_height
    self.x = int(self.screen_width/2)
    self.y = int(self.screen_height/2)
    self.arbeiter = Arbeiter()
    self.vx = 0
    self.vy = 0
    self.map_file = PhotoImage(file="Map.png")
    self.object = self.canvas.create_image(self.x, self.y, image = self.map_file)
    self.minimap = Minimap(self.canvas, self.screen_width, self.screen_height)
    arty_coords = self.arty_spawn()
    arty_x = arty_coords[0]
    arty_y = arty_coords[1]
    arty_picture_x = arty_x-2500
    arty_picture_y = arty_y-2500
    self.arty = Artillery(self.canvas, self.window, self.period, arty_picture_x, arty_picture_y, self.screen_width, self.screen_height)
    
  def move(self, vx, vy):
    self.canvas.move(self.object, -vx, -vy)
    self.canvas.move(self.arty.object, -vx, -vy)
    self.minimap.show_player(vx,vy)

  def arty_spawn(self):
    off_x=130
    off_y=60
    points = [[off_x,off_y],[off_x,0],[off_x,-off_y],[0,off_y],[0,0],[0,-off_y],[-off_x,off_y],[-off_x,0],[-off_x,-off_y]]
    free_position = False
    while free_position != True:
      x = randint(1100,3900)
      y = randint(600,4400)
      free_position = True
      for point in points:
        free_point = self.arbeiter.is_this_point_free(x+point[0],y+point[1])
        if free_point == False:
            free_position = False
            break  
    self.minimap.show_arty(x,y)
    return([x, y])
      
      
