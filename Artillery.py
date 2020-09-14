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

class Artillery: 
  def __init__(self, canvas, window, period, x, y, screen_width, screen_height):
    self.canvas = canvas
    self.window = window
    self.period = period
    self.screen_width = screen_width
    self.screen_height = screen_height
    self.x = x
    self.y = y
    self.arty_file = PhotoImage(file="Conqueror_GC.png")
    self.object = self.canvas.create_image(self.x + 0.5*self.screen_width, self.y + 0.5*self.screen_height, image = self.arty_file)
