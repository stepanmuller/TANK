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

from tank_player_turret import Turret
from keyboard import Keyboard 
from tank_physics import Physics

class Tank:  
  def __init__(self, canvas, window, period, screen_width, screen_height):
    #physics specs:
    self.mass = 188980 #kg
    self.power = 200*745  #W, original 1750*745
    self.hull_traverse = 30 #16 #deg/s
    self.turret_traverse = 50 #17 #deg/s
    self.top_speed_forwards=30/3.6 #m/kg
    self.top_speed_backwards=15/3.6 #m/kg
    #end
    self.canvas = canvas
    self.window = window
    self.period = period
    self.screen_width = screen_width
    self.screen_height = screen_height
    self.keyboard = Keyboard(self.window)
    self.physics = Physics(self.period, self.mass, self.power, self.hull_traverse, self.turret_traverse, self.top_speed_forwards, self.top_speed_backwards)
    self.x = 2500
    self.y = 2500
    self.default_x = int(self.screen_width/2) #position in the middle which does not change
    self.default_y = int(self.screen_height/2) #position in the middle which does not change
    self.vx = 0
    self.vy = 0
    self.hull_traverse = 0
    self.angle = 0
    self.turret_position = 35
    self.velocity = 0 #m/s
    self.turret_x = self.default_x+(sin(radians(self.angle))*self.turret_position)
    self.turret_y = self.default_y+(cos(radians(self.angle))*self.turret_position)
    self.hull_picture = Image.open('Hull.png')
    self.rotated_hull = ImageTk.PhotoImage(self.hull_picture.rotate(self.angle))
    self.object = self.canvas.create_image(self.x, self.y, image = self.rotated_hull)
    self.turret = Turret(self.canvas, self.window, self.turret_x, self.turret_y, self.period, self.physics.turret_traverse, self.screen_width, self.screen_height)
    self.turret.map_x = self.x+(sin(radians(self.angle))*self.turret_position)
    self.turret.map_y = self.y+(cos(radians(self.angle))*self.turret_position)
    self.velocity_indicator = self.canvas.create_text(20,self.screen_height-20,text=str(int(self.velocity*3.6)))
    self.show()
  
  def move(self):
    move_list=self.physics.drive(self.velocity, self.keyboard.pressed)
    self.velocity = self.velocity + move_list[0]
    self.canvas.delete(self.velocity_indicator)
    self.velocity_indicator = self.canvas.create_text(20,self.screen_height-20,text=str(int(self.velocity*3.6)))
    self.hull_traverse = move_list[1]
    self.vx = (sin(radians(self.angle + (0.5 * self.hull_traverse))) * - (self.velocity * 20*(1/self.period)))
    self.vy = (cos(radians(self.angle + (0.5 * self.hull_traverse))) * - (self.velocity * 20*(1/self.period)))
    #adding recoil from shot
    self.vx = self.vx + self.turret.recoil_x
    self.vy = self.vy + self.turret.recoil_y
    self.x = self.x + self.vx
    self.y = self.y + self.vy
    self.angle = self.angle + self.hull_traverse
    self.turret.x = self.default_x + (sin(radians(self.angle)) * self.turret_position)
    self.turret.y = self.default_y + (cos(radians(self.angle)) * self.turret_position)
    self.turret.map_x = self.x+(sin(radians(self.angle))*self.turret_position)
    self.turret.map_y = self.y+(cos(radians(self.angle))*self.turret_position)
  
  def show(self):
    self.rotated_hull = ImageTk.PhotoImage(self.hull_picture.rotate(self.angle))
    self.canvas.delete(self.object)
    self.object = self.canvas.create_image(self.default_x, self.default_y, image=self.rotated_hull)
    self.turret.move(self.hull_traverse)
