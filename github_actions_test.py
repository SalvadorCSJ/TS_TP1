from math import sqrt

class Point:
  def __init__(self,x_value:int,y_value:int):
    self.x = x_value
    self.y = y_value

  def get_values(self):
    return (self.x,self.y)

  def calculate_distance(self,a:'Point') -> float:
    a_x,a_y = a.get_values()
    return sqrt((self.x-a_x)**2 + (self.y-a_y)**2)
