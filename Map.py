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

class Map:  
  def __init__(self, canvas, window, period, screen_width, screen_height):
    self.canvas = canvas
    self.window = window
    self.period = period
    self.screen_width = screen_width
    self.screen_height = screen_height
    self.x = int(self.screen_width/2)
    self.y = int(self.screen_height/2)
    self.vx = 0
    self.vy = 0
    self.map_picture = PhotoImage(file="Map.png")
    self.object = self.canvas.create_image(self.x, self.y, image = self.map_picture)
    #temporary testing of a crashing algorithm here:
    object_x = int(self.screen_width/2)
    object_y = int(self.screen_height/2) - 400
    self.rectangle = self.canvas.create_rectangle(object_x - 2500, object_y, object_x + 2500, object_y + 50, fill = "red")
    self.text = self.canvas.create_text(object_x, object_y + 25, text = "You shall not pass", font=("Arial", 25), fill = "black")
    #end
    
  def move(self, vx, vy):
    self.canvas.move(self.object, -vx, -vy)
    #temporary testing of a crashing algorithm here:
    self.canvas.move(self.rectangle, -vx, -vy)
    self.canvas.move(self.text, 0, -vy)
    #end
