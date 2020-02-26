from tkinter import *
import tkinter as tk

class Physics:
  def __init__(self, period):
    self.mass = 188980 #kg
    self.power = 300*745  #W, original 1750*745
    self.brake_power = 3000000 #W
    self.hull_traverse = 30 #16 #deg/s
    self.turret_traverse = 50 #17 #deg/s
    self.top_speed_forwards=20/3.6 #m/kg
    self.top_speed_backwards=10/3.6 #m/kg
    self.period=period #ms
    
  def drive(self, velocity, keys):
    #steering
    hull_traverse=0
    if "a" in keys:
      hull_traverse = hull_traverse + self.hull_traverse * (self.period / 1000)
    if "d" in keys:
      hull_traverse = hull_traverse - self.hull_traverse * (self.period / 1000)
    #forwards/backwards
    real_velocity = velocity
    if abs(velocity) < 1:
      if velocity >= 0:
          velocity = 1
      else:
          velocity = - 1
    if "w" in keys and "s" not in keys:
      if velocity < 0: #brake
          acceleration = self.brake_power / self.mass
      else:
          acceleration = ((self.power / abs(velocity)) * (self.top_speed_forwards - abs(velocity))) / self.mass
      if abs(acceleration)* (self.period / 1000) > self.top_speed_forwards:
          acceleration = self.top_speed_forwards
    elif "s" in keys and "w" not in keys:
      hull_traverse=-hull_traverse
      if velocity > 0: #brake
          acceleration = - self.brake_power / self.mass
      else:
          acceleration = - ((self.power / abs(velocity)) * (self.top_speed_backwards - abs(velocity))) / self.mass
      if abs(acceleration)* (self.period / 1000) > self.top_speed_backwards:
          acceleration = - self.top_speed_backwards
    elif ("w" not in keys and "s" not in keys) or ("w" in keys and "s" in keys):
      if real_velocity>0:
        acceleration = - 500000 / self.mass
        if (real_velocity + acceleration) < 0:
            acceleration = - real_velocity
      else:
        acceleration = 500000 / self.mass
        if (real_velocity + acceleration) < 0:
            acceleration = - real_velocity
    acceleration = acceleration * (self.period / 1000)
    return [acceleration, hull_traverse]
