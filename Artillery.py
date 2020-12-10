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
import callouts

class Artillery: 
  def __init__(self, canvas, window, period, screen_width, screen_height):
    self.canvas = canvas
    self.window = window
    self.period = period
    self.screen_width = screen_width
    self.screen_height = screen_height
    self.x = 0
    self.y = 0
    self.player_x = 0
    self.player_y = 0
    self.turret_angle = 0
    self.turret_traverse = 85 * (self.period/1000)
    self.dead = False
    self.arty_hull_file = PhotoImage(file="Arty_hull.png")
    self.arty_turret_file = Image.open("Arty_turret.png")
    self.explosion_file = PhotoImage(file="Arty_explosion.png")
  def update_turret(self, vx, vy):
    if self.dead == False:
      if self.turret_angle > 180:
        self.turret_angle = self.turret_angle - 360
      elif self.turret_angle <= - 180:
        self.turret_angle = self.turret_angle + 360
      self.turret_x = self.turret_x + vx
      self.turret_y = self.turret_y + vy
      #self.player_y = relative position of the tank to center of the map
      #self.y = relative position of the artillery to center of the map
      self.relative_y = self.player_y - self.y + self.screen_height/2
      self.relative_x = self.player_x - self.x + self.screen_width/2
      if self.relative_x == 0:
        self.relative_x == 0.00000001
      if self.relative_y == 0:
        self.relative_y = 0.00000001
      enemy_angle = degrees(atan(self.relative_x/self.relative_y))
      if self.relative_y > 0:
        if self.relative_x < 0:
          enemy_angle = enemy_angle + 180
        else:
          enemy_angle = enemy_angle - 180
      delta = self.turret_move(enemy_angle)
      if abs(delta) > 0.5 * self.turret_traverse:
        if delta > 0:
          self.turret_angle = self.turret_angle + self.turret_traverse
        else:
          self.turret_angle = self.turret_angle - self.turret_traverse
      self.rotated_turret = ImageTk.PhotoImage(self.arty_turret_file.rotate(self.turret_angle))
      self.turret_picture = self.canvas.create_image(self.turret_x+5, self.turret_y, image = self.rotated_turret)
  
  def turret_move(self, enemy_angle):
    delta = enemy_angle-self.turret_angle 
    if enemy_angle * self.turret_angle >= 0:
      return delta
    if enemy_angle > 0: 
      enemy_angle = enemy_angle - 180
    else:
      enemy_angle = enemy_angle + 180
    delta = enemy_angle - self.turret_angle
    delta = - delta
    return delta
    
  def shoot(self):
    if self.dead == False:
      target_x = self.screen_width/2
      target_y = self.screen_height/2
      my_x = target_x - self.relative_x
      my_y = target_y - self.relative_y
      self.shell = Shell(self.canvas, self.window, target_x, target_y, my_x, my_y)
      self.window.after(5000, self.shoot)
      
  def die(self):
    if self.dead==False:
        self.dead = True
        pygame.mixer.music.load("arty_explosion.wav")
        pygame.mixer.music.play()
        coords = self.canvas.coords(self.object)
        self.canvas.delete(self.object)
        self.explosion_picture = self.canvas.create_image(coords[0], coords[1]-50, image = self.explosion_file)
        self.window.after(200, self.delete_explosion)
        
  def spawn(self, x, y):
    self.x = x
    self.y = y
    self.turret_x = self.x
    self.turret_y = self.y
    self.object = self.canvas.create_image(self.x, self.y, image = self.arty_hull_file)
    self.x = self.x + self.player_x
    self.y = self.y + self.player_y
    self.dead = False
    self.update_turret(0,0)
    self.window.after(2500, self.shoot)
    
  def delete_explosion(self):
    self.canvas.delete(self.explosion_picture)
    self.window.after(1200, self.play_death_sound)
    
  def play_death_sound(self):
    n_effects=4
    chosen = randint(1, n_effects)
    pygame.mixer.music.load('arty_death_' + str(chosen) + ".wav")
    pygame.mixer.music.play()
    
    
class Shell:
  def __init__(self, canvas, window, target_x, target_y, my_x, my_y):
    self.canvas = canvas
    self.window = window
    self.target_x = target_x
    self.target_y = target_y
    self.my_x = my_x
    self.my_y = my_y
    print("oh hi mark")
