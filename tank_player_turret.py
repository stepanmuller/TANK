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
pygame.init()  

class Turret:
  def __init__(self, canvas, window, x, y, period, traverse, screen_width, screen_height):
    self.turret_traverse = traverse * (period / 1000)
    self.canvas = canvas
    self.window = window
    self.screen_width = screen_width
    self.screen_height = screen_height
    self.aiming_circle_image=PhotoImage(file="Aiming_circle.png")
    self.window.bind("<Button-1>", self.shoot)
    self.period = period
    self.x = x
    self.y = y
    self.recoil_x = 0
    self.recoil_y = 0
    self.angle = 0
    self.turret_picture = Image.open('Turret.png')
    self.reload_time = 5 #s
    self.running_reload_sound = False
    self.reload_speed = (360 * self.period) / (1000 * self.reload_time) #degrees per period
    self.loaded_degrees = 0
    self.aiming_circle = self.canvas.create_image(self.x, self.y, image = self.aiming_circle_image)
    self.reload_circle_red = self.canvas.create_oval(self.x - 16, 
        self.y - 16, self.x + 16, self.y + 16, fill = "red", width = 0)
    self.reload_arc = self.canvas.create_arc(self.x - 16, 
        self.y - 16, self.x + 16, self.y + 16, fill = "green", width = 0, extent = self.loaded_degrees)
    self.reload_circle_white = self.canvas.create_oval(self.x - 12, 
        self.y - 13, self.x + 13, self.y + 13, fill = "white", width = 0)
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
    if abs(delta)>3:
        self.reload(mouse.x, mouse.y, False)
    else:
        self.reload(mouse.x, mouse.y, True)
    self.show()
  
  def show(self):
    self.rotated_turret = ImageTk.PhotoImage(self.turret_picture.rotate(self.angle))
    self.canvas.delete(self.object)
    self.object = self.canvas.create_image(self.x, self.y, image = self.rotated_turret)
    
  def reload(self, x, y, aimed):
    white_circle_fill = "white"
    if self.loaded_degrees > - 359 and self.loaded_degrees <=0:
        self.loaded_degrees = self.loaded_degrees - self.reload_speed
    else:
        self.window.bind("<Button-1>", self.shoot)
        self.loaded_degrees = 359
        white_circle_fill = "green"
    if self.loaded_degrees < -359:
        self.loaded_degrees = -359
    remaining_time = ((360 + self.loaded_degrees) * self.period) / (self.reload_speed * 1000)
    if remaining_time <= 1.3 and self.running_reload_sound == False:
        pygame.mixer.music.load("Reload_sound.wav")
        pygame.mixer.music.play()
        self.running_reload_sound = True
    if (self.reload_time - remaining_time) >= 0.15:
        self.recoil_x = 0
        self.recoil_y = 0
    self.canvas.delete(self.reload_circle_red)
    self.canvas.delete(self.reload_arc)
    self.canvas.delete(self.reload_circle_white)
    self.canvas.delete(self.aiming_circle)
    if aimed == True:
        self.aiming_circle = self.canvas.create_image(x, y, image = self.aiming_circle_image)
    self.reload_circle_red = self.canvas.create_oval(x - 16, 
        y - 16, x + 16, y + 16, fill = "red", width = 0)
    self.reload_arc = self.canvas.create_arc(x - 16, 
        y - 16, x + 16, y + 16, fill = "green", width = 0, extent = self.loaded_degrees)  
    self.reload_circle_white = self.canvas.create_oval(x - 13, 
        y - 13, x + 13, y + 13, fill = white_circle_fill , width = 0)
    
  def shoot(self, event=None):
    self.window.unbind("<Button-1>")
    self.loaded_degrees = 0
    self.shell = Shell(self.canvas, self.window, self.x, self.y, self.angle, self.period, self.screen_width, self.screen_height)
    self.recoil_x = -0.08 * self.shell.vx
    self.recoil_y = -0.08 * self.shell.vy
    self.running_reload_sound = False
    pygame.mixer.music.load("Gun_sound.wav")
    pygame.mixer.music.play()
    #playsound("Gun_sound.wav", block = False)
    
class Shell:
  def __init__(self, canvas, window, x, y, angle, period, screen_width, screen_height):
    self.canvas = canvas
    self.window = window
    self.screen_width = screen_width
    self.screen_height = screen_height
    self.angle = angle
    self.x = x + cos(radians(- self.angle - 90)) * 160
    self.y = y + sin(radians(- self.angle - 90)) * 160
    self.period = period
    self.velocity = (self.period / 1000) * 1500 #pixels/period
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
    if self.x > -20 and self.x < self.screen_width + 20 and self.y > -20 and self.y < self.screen_height + 20:
        self.shell_picture = self.canvas.create_image(self.x, self.y, image = self.rotated_shell)
        self.window.after(self.period, self.fly)
  
  def delete_smoke(self):
    self.canvas.delete(self.smoke)

