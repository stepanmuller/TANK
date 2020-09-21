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
    self.arty_file = PhotoImage(file="Conqueror_GC.png")
    self.explosion_file = PhotoImage(file="Arty_explosion.png")
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
    self.object = self.canvas.create_image(self.x, self.y, image = self.arty_file)
    self.dead = False
  def delete_explosion(self):
    self.canvas.delete(self.explosion_picture)
    self.window.after(500, self.play_death_sound)
  def play_death_sound(self):
    n_effects=5
    chosen = randint(1, n_effects)
    pygame.mixer.music.load("arty_death_" + chosen + ".wav")
    pygame.mixer.music.play()
