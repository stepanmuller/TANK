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


class Calculator:
  def __init__(self):
    #points are in polar coords: total distance from center and angle from y axis 
    point_top_L = [96, 23]
    point_top_R = [96, -23]
    point_center_L = [36, 90]
    point_center_R = [36, -90]
    point_bottom_L = [103, 160]
    point_bottom_R = [103, -160]
    point_top_center = [89, 0]
    point_bottom_center = [97, 180]
    self.point_list = [point_top_L, point_top_R, point_center_L, point_center_R, point_bottom_L, point_bottom_R, point_top_center, point_bottom_center]
  
  def calculate_tank_points(self, center_x, center_y, angle):
    newpoints = []
    for point in self.point_list:
        new_angle = point[1] + angle
        newpoints.append([point[0],new_angle])
    points_xy_coords = []
    for point in newpoints:
        x = sin(radians(point[1])) * point[0]
        y = cos(radians(point[1])) * point[0]
        x = center_x + x
        y = center_y + y
        points_xy_coords.append([x,y])
    return points_xy_coords

