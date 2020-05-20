#http:/tkinter.programujte.com

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

from tank_player_main import Tank
from Map import Map
from Json_arbeiter import Arbeiter

class Game:
  def __init__(self):
    self.window = Tk()
    self.screen_width = self.window.winfo_screenwidth()
    self.screen_height = self.window.winfo_screenheight()
    self.canvas = Canvas(self.window, width = self.screen_width, height = self.screen_height, bg="white")
    self.canvas.place(relx = 0, rely = 0, anchor=NW)
    self.window.bind("<Escape>", self.end)
    self.window.attributes("-fullscreen", True)
    self.window.wm_attributes("-topmost", 1)
    self.window.focus_set()
    self.period = 20
    self.tank = Tank(self.canvas, self.window, self.period, self.screen_width, self.screen_height)
    self.map = Map(self.canvas, self.window, self.period, self.screen_width, self.screen_height)
    self.arbeiter = Arbeiter()
    self.crash = False
    self.step()
  
  def step(self):
    original_x = self.tank.x
    original_y = self.tank.y
    original_angle = self.tank.angle
    self.tank.move() #this calculates the future position of the tank
    free_point = self.arbeiter.is_this_point_free(self.tank.x,self.tank.y)
    if free_point == False:
        self.tank.x = original_x
        self.tank.y = original_y
        self.tank.angle = original_angle
        self.tank.velocity = 0
        self.tank.vx = 0
        self.tank.vy = 0
    self.tank.show() #this rotates the tank picture
    self.map.move(self.tank.vx, self.tank.vy) #this moves the map picture
    
    self.window.after(self.period,self.step)
  
  def end(self, event = None):
    self.window.destroy()
  


        
tankgame = Game()

mainloop()

