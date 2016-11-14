from Behavior import Behavior
from motor_rec import Motor_Rec

class Derp(Behavior):
  def __init__(self, static_priority):
    super().__init__([], True, static_priority)
    self.forward = True

  def get_update(self):
    self.forward = not self.forward
    if self.forward:
      print('FORWARD!!!!')
      return Motor_Rec(9, 0, 1, 2)
    else:
      print('NOT FORWARD!!!!')
      return Motor_Rec(9, 0, -1, 2)
