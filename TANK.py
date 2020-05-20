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
import json

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
    self.arbeiter = Arbeiter(self.screen_width, self.screen_height)
    self.crash = False
    self.step()
    with open('obstructions.txt') as json_file:
        self.data = json.load(json_file)
  
  def step(self):
    #here we need to identify a FUTURE crash --> use tank.vx and tank.vy to predict next position
    #because if we stop the tank at PRESENT crash it wont be able to go backwards
    #if crash is going to happen, self.tank.velocity must be changed to 0
    #temporary testing of a crashing algorithm here:
    if self.crash == False:     #not crashed yet
        self.tank.move()
        if self.tank.y + self.tank.vy <=int(self.screen_height/2) - 250:
            self.crash = True
            self.tank.velocity = 0
            self.tank.vx = 0
            self.tank.vy = 0
        else:
            self.map.move(self.tank.vx, self.tank.vy)
    else:   #already crashed
        self.tank.velocity = 0
        self.tank.move()
        if self.tank.vy>0:
            self.map.move(self.tank.vx, self.tank.vy)
            self.crash = False
    #end, not quite working yet
    
    # original code: self.tank.move()
    # original code: self.map.move(self.tank.vx, self.tank.vy)
    self.window.after(self.period,self.step)
  
  def end(self, event = None):
    self.window.destroy()
  


        
tankgame = Game()

mainloop()

