from github_actions_test import Point

def test_generating_point():
  a = Point(3,4)
  assert a != None

def test_point_parameters_initialization():
  a = Point(3,4)
  x,y = a.get_values()
  assert x == 3
  assert y == 4

def test_distance_calculation():
  a = Point(3,4)
  b = Point(6,8)
  assert a.calculate_distance(b) == 5
