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
    self.dead = False
    self.arty_hull_file = PhotoImage(file="Arty_hull.png")
    self.arty_turret_file = Image.open("Arty_turret.png")
    self.explosion_file = PhotoImage(file="Arty_explosion.png")
  def update_turret(self, vx, vy):
    if self.dead == False:
      self.turret_x = self.turret_x + vx
      self.turret_y = self.turret_y + vy
      #self.player_y = relative position of the tank to center of the map
      #self.y = relative position of the artillery to center of the map
      player_y = self.player_y - self.y + self.screen_height/2
      player_x = self.player_x - self.x + self.screen_width/2
      self.turret_angle = degrees(atan(player_x/player_y)) - 90
      if player_y > 0:
        self.turret_angle = self.turret_angle + 180
      self.rotated_turret = ImageTk.PhotoImage(self.arty_turret_file.rotate(self.turret_angle))
      self.turret_picture = self.canvas.create_image(self.turret_x+5, self.turret_y, image = self.rotated_turret)
      print(self.turret_x, self.turret_y)
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
  def delete_explosion(self):
    self.canvas.delete(self.explosion_picture)
    self.window.after(1200, self.play_death_sound)
  def play_death_sound(self):
    n_effects=4
    chosen = randint(1, n_effects)
    pygame.mixer.music.load('arty_death_' + str(chosen) + ".wav")
    pygame.mixer.music.play()


