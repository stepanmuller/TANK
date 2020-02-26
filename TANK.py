#http:/tkinter.programujte.com

from tkinter import *
from random import randint
import sys
import os
import tkinter as tk
from PIL import ImageTk
from PIL import Image
from math import *
import pyautogui
from keyboard import Keyboard 
from tank_physics import Physics


###
class Game:
  def __init__(self):
    self.window = Tk()
    self.canvas = Canvas(self.window, width=1024,height=768, bg="white")
    self.canvas.place(relx=0, rely=0, anchor=NW)
    self.window.bind("<Escape>", self.end)
    self.window.attributes("-fullscreen", True)
    self.window.wm_attributes("-topmost", 1)
    self.window.focus_set()
    self.period = 20
    self.tank = Tank(self.canvas, self.window, self.period)
    self.step()
  
  def step(self):
    self.tank.move()
    self.window.after(self.period,self.step)
  
  def end(self, event = None):
    self.window.destroy()

###
class Tank:  
  def __init__(self, canvas, window, period):
    ###
    self.canvas = canvas
    self.window = window
    self.period = period
    self.keyboard = Keyboard(self.window)
    self.physics = Physics(self.period)
    self.x = 512
    self.y = 350
    self.angle = 0
    self.turret_position = 35
    self.velocity = 0 #m/s
    self.turret_x = self.x+(sin(radians(self.angle))*self.turret_position)
    self.turret_y = self.y+(cos(radians(self.angle))*self.turret_position)
    self.hull_picture = Image.open('Hull.png')
    self.rotated_hull = ImageTk.PhotoImage(self.hull_picture.rotate(self.angle))
    self.object = self.canvas.create_image(self.x, self.y, image = self.rotated_hull)
    self.turret = Turret(self.canvas, self.window, self.turret_x, self.turret_y, self.period, self.physics.turret_traverse)
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

###    
class Turret:
  def __init__(self, canvas, window, x, y, period, traverse):
    self.turret_traverse = traverse * (period / 1000)
    self.canvas = canvas
    self.window = window
    self.window.bind("<Button-1>", self.shoot)
    self.period = period
    self.x = x
    self.y = y
    self.angle = 0
    self.turret_picture = Image.open('Turret.png')
    self.rotated_turret = ImageTk.PhotoImage(self.turret_picture.rotate(self.angle))
    self.object = self.canvas.create_image(self.x, self.y, image = self.rotated_turret)
  
  def turret_move(self, mouse_angle):
    delta = mouse_angle-self.angle 
    if mouse_angle * self.angle >= 0:
      return delta
    if mouse_angle > 0: 
      mouse_angle = mouse_angle - 180
    else:
      mouse_angle = mouse_angle + 180
    delta = mouse_angle - self.angle
    delta = - delta
    return delta
    
  def move(self, hull_traverse):
    self.angle = self.angle + hull_traverse
    if self.angle > 180:
      self.angle = self.angle - 360
    elif self.angle <= - 180:
      self.angle = self.angle + 360
    mouse = pyautogui.position()
    dy = mouse.y - self.y
    dx = mouse.x - self.x
    if dy == 0:
      dy = 0.0000000001
    if dx == 0:
      dx = 0.0000000001
    mouse_angle = degrees(atan(dx/dy))
    if dy > 0:
      if dx < 0:
        mouse_angle = mouse_angle + 180
      else:
        mouse_angle = mouse_angle - 180
    delta = self.turret_move(mouse_angle)
    if abs(delta) > 0.5 * self.turret_traverse:
      if delta > 0:
        self.angle = self.angle + self.turret_traverse
      else:
        self.angle = self.angle - self.turret_traverse
    self.show()
  
  def show(self):
    self.rotated_turret = ImageTk.PhotoImage(self.turret_picture.rotate(self.angle))
    self.canvas.delete(self.object)
    self.object = self.canvas.create_image(self.x, self.y, image = self.rotated_turret)
    
  def shoot(self, event=None):
    self.shell = Shell(self.canvas, self.window, self.x, self.y, self.angle, self.period)

class Shell:
  def __init__(self, canvas, window, x, y, angle, period):
    self.canvas = canvas
    self.window = window
    self.angle = angle
    self.x = x + cos(radians(- self.angle - 90)) * 160
    self.y = y + sin(radians(- self.angle - 90)) * 160
    self.period = period
    self.velocity = (self.period / 1000) * 1000 #pixels/period
    self.vx = cos(radians(-self.angle-90)) * self.velocity
    self.vy = sin(radians(-self.angle-90)) * self.velocity
    self.shell_picture = Image.open('Shell.png')
    self.smoke_picture = Image.open('Smoke.png')
    self.rotated_shell = ImageTk.PhotoImage(self.shell_picture.rotate(self.angle))
    self.rotated_smoke = ImageTk.PhotoImage(self.smoke_picture.rotate(self.angle))
    self.shell_picture = self.canvas.create_image(self.x, self.y, image = self.rotated_shell)
    self.smoke = self.canvas.create_image(self.x, self.y, image = self.rotated_smoke)
    self.fly()
    self.window.after(100, self.delete_smoke)
  
  def fly(self):
    self.x = self.x + self.vx
    self.y = self.y + self.vy
    self.canvas.delete(self.shell_picture)
    if self.x > -20 and self.x < 1044 and self.y > -20 and self.y < 788:
        self.shell_picture = self.canvas.create_image(self.x, self.y, image = self.rotated_shell)
        self.window.after(self.period, self.fly)
  
  def delete_smoke(self):
    self.canvas.delete(self.smoke)
        
tankgame = Game()

mainloop()

