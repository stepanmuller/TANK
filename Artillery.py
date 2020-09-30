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
    self.explosion_file = PhotoImage(file="Arty_explosion.png")
  def update_turret(self):
    if self.dead == False:
      print()
      print("self.player_y " + str(self.player_y))
      print("self.screen_height*0.5 " + str(self.screen_height*0.5))
      print("self.y " + str(self.y))
      self.player_y = self.player_y - 0.5*self.screen_height + self.y - 2500
      print(self.player_x, self.player_y)
      self.window.after(self.period, self.update_turret)
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
    self.object = self.canvas.create_image(self.x, self.y, image = self.arty_hull_file)
    self.dead = False
    self.update_turret()
  def delete_explosion(self):
    self.canvas.delete(self.explosion_picture)
    self.window.after(1200, self.play_death_sound)
  def play_death_sound(self):
    n_effects=4
    chosen = randint(1, n_effects)
    pygame.mixer.music.load('arty_death_' + str(chosen) + ".wav")
    pygame.mixer.music.play()


