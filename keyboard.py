from tkinter import *
import tkinter as tk

class Keyboard:
  def __init__(self, window):
    self.pressed = []
    self.window = window
    self.window.bind_all('<KeyPress>', self.handle_key_down)
    self.window.bind_all('<KeyRelease>', self.handle_key_up)
    self.window.bind_all("<Button-3>", self.handle_mouse_down)
    self.window.bind_all("<ButtonRelease-3>", self.handle_mouse_up)
  
  def is_pressed(self, key):
    if key in self.pressed:
      return True
    return False
    
  def handle_key_down(self, event):
    key = str(event.keysym)
    if key not in self.pressed:
      self.pressed.append(key)
    
  def handle_key_up(self, event):
    key = str(event.keysym)
    if key in self.pressed:
      self.pressed.remove(key)
      
  def handle_mouse_down(self, event):
    if "Button-3" not in self.pressed:
      self.pressed.append("Button-3")
      
  def handle_mouse_up(self, event):
    if "Button-3" in self.pressed:
      self.pressed.remove("Button-3")
