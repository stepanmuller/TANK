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
    with open('obstruction.txt') as json_file: 
      self.data = json.load(json_file)["obstruction"]
  
  def is_this_point_free(self, X, Y):
    I=0
    J=0
    for a in range(10):
      if ((X+a)%10)==0:
        J=(X+a)/10
      if ((Y+a)%10)==0:
        I=(Y+a)/10
    return(self.data[int(I)][int(J)])
