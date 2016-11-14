from Behavior import Behavior
from motor_rec import Motor_Rec
from ultrasonic import *


class WatchOutForTheWall(Behavior):
  def __init__(self, sensobs, static_pri):
    super().__init__(sensobs, True, static_pri)

  def get_update(self):
    action = 0.25;
    score=10;
    distance = self.sensobs['ultrasonic'].get_value()
    print(distance)

    if(distance<10 and distance>0):
      self.active_flag = True
      degrees = 180 - 18*distance;
      action = ["r",degrees];
    else:
      self.active_flag = False
    return Motor_Rec(10, action, 'watchOutForTheWall - distance:' + str(distance))
