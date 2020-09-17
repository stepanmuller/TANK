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
  def __init__(self):
    self.arty_list = []
    with open('obstruction.txt') as json_file: 
      self.data = json.load(json_file)["obstruction"]
  
  def is_this_point_free(self, X, Y):
    if [int(X),int(Y)] in self.arty_list:
      
      return False
    return(bool(self.data[int(Y)][int(X)]))
    
  def spawn_arty(self, x_center, y_center, off_x, off_y):
    for x in range(x_center - off_x, x_center + off_x):
      for y in range(y_center - off_y, y_center + off_y):
        self.arty_list.append([x, y])

