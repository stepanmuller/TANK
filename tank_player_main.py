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
    self.canvas = canvas
    self.window = window
    self.period = period
    self.screen_width = screen_width
    self.screen_height = screen_height
    self.keyboard = Keyboard(self.window)
    self.physics = Physics(self.period)
    self.x = int(self.screen_width/2)
    self.y = int(self.screen_height/2)
    self.angle = 0
    self.turret_position = 35
    self.velocity = 0 #m/s
    self.turret_x = self.x+(sin(radians(self.angle))*self.turret_position)
    self.turret_y = self.y+(cos(radians(self.angle))*self.turret_position)
    self.hull_picture = Image.open('Hull.png')
    self.rotated_hull = ImageTk.PhotoImage(self.hull_picture.rotate(self.angle))
    self.object = self.canvas.create_image(self.x, self.y, image = self.rotated_hull)
    self.turret = Turret(self.canvas, self.window, self.turret_x, self.turret_y, self.period, self.physics.turret_traverse, self.screen_width, self.screen_height)
    self.show()
  
  def move(self):
    move_list=self.physics.drive(self.velocity, self.keyboard.pressed)
    self.velocity = self.velocity + move_list[0]
    hull_traverse = move_list[1]
    vx = (sin(radians(self.angle + (0.5 * hull_traverse))) * - (self.velocity * 20*(1/self.period)))
    vy = (cos(radians(self.angle + (0.5 * hull_traverse))) * - (self.velocity * 20*(1/self.period)))
    self.x = self.x + vx
    self.y = self.y + vy
    self.angle = self.angle + hull_traverse
    self.turret.x = self.x + (sin(radians(self.angle)) * self.turret_position)
    self.turret.y = self.y + (cos(radians(self.angle)) * self.turret_position)
    self.show()
    self.turret.move(hull_traverse)
  
  def show(self):
    self.rotated_hull = ImageTk.PhotoImage(self.hull_picture.rotate(self.angle))
    self.canvas.delete(self.object)
    self.object = self.canvas.create_image(self.x, self.y, image=self.rotated_hull)
