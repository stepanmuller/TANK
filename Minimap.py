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

class Minimap:
  def __init__(self, canvas, screen_width, screen_height):
    self.canvas = canvas
    self.screen_width = screen_width
    self.screen_height = screen_height
    self.minimap_file = PhotoImage(file="Minimap.png")
    self.minimap = self.canvas.create_image(self.screen_width-125, self.screen_height-125, image = self.minimap_file)
    self.player_x = 2500
    self.player_y = 2500
    self.arty_x = 0
    self.arty_y = 0
    self.player_picture_x = self.player_x/20 + self.screen_width - 250
    self.player_picture_y = self.player_y/20 + self.screen_height - 250
    self.arty_picture_x = self.arty_x/20 + self.screen_width - 250
    self.arty_picture_y = self.arty_y/20 + self.screen_height - 250
    self.player = self.canvas.create_rectangle(self.player_picture_x+1, self.player_picture_y+1, self.player_picture_x-1, self.player_picture_y-1, fill="black")
    self.arty = self.canvas.create_rectangle(self.arty_picture_x+1, self.arty_picture_y+1, self.arty_picture_x-1, self.arty_picture_y-1, fill="red", outline="red")
  
  def show_player (self, player_vx, player_vy):
    self.canvas.delete(self.minimap)
    self.minimap = self.canvas.create_image(self.screen_width-125, self.screen_height-125, image = self.minimap_file)
    self.canvas.delete(self.arty)
    self.arty = self.canvas.create_rectangle(self.arty_picture_x+1, self.arty_picture_y+1, self.arty_picture_x-1, self.arty_picture_y-1, fill="red", outline="red")
    self.player_x = self.player_x + player_vx
    self.player_y = self.player_y + player_vy
    self.player_picture_x = self.player_x/20 + self.screen_width - 250
    self.player_picture_y = self.player_y/20 + self.screen_height - 250
    self.canvas.delete(self.player)
    self.player = self.canvas.create_rectangle(self.player_picture_x+1, self.player_picture_y+1, self.player_picture_x-1, self.player_picture_y-1, fill="black")
    
  def show_arty (self, arty_x, arty_y):
    self.minimap = self.canvas.create_image(self.screen_width-125, self.screen_height-125, image = self.minimap_file)
    self.arty_x = arty_x
    self.arty_y = arty_y
    self.arty_picture_x = self.arty_x/20 + self.screen_width - 250
    self.arty_picture_y = self.arty_y/20 + self.screen_height - 250
    self.canvas.delete(self.arty)
    self.arty = self.canvas.create_rectangle(self.arty_picture_x+1, self.arty_picture_y+1, self.arty_picture_x-1, self.arty_picture_y-1, fill="red", outline="red")
   
