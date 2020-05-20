#http:/tkinter.programujte.com

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
import json


class Arbeiter:
  def __init__(self, screen_width, screen_height):
    self.screen_width = screen_width
    self.screen_height = screen_height
  
  def is_this_point_free(self):
    print("Drahous")
