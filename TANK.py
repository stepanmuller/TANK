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
    self.step()
  
  def step(self):
    self.tank.move()
    self.map.move(self.tank.vx, self.tank.vy)
    self.window.after(self.period,self.step)
  
  def end(self, event = None):
    self.window.destroy()


        
tankgame = Game()

mainloop()

