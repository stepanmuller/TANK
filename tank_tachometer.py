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

class Tachometer:
  def __init__(self, canvas, screen_height):
    self.canvas = canvas
    self.screen_height = screen_height
    self.tachometer_picture = PhotoImage(file="Tachometer.png")
    self.background = self.canvas.create_image(40, self.screen_height-38, image = self.tachometer_picture)
    self.velocity_number = self.canvas.create_text(42,self.screen_height-37,text=str(0))
  def show (self, velocity):
    self.canvas.delete(self.velocity_number)
    self.velocity_number = self.canvas.create_text(42,self.screen_height-37,text=str(int(velocity*3.6)), fill = "white", font = ("Helvetica", 15))
