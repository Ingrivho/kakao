from Behavior import Behavior
from motor_rec import Motor_Rec
from reflectance_sensors import *

class TurnAtEdge(Behavior):
   
    def __init__(self, sensobs, pri):
            super().__init__(sensobs, True, pri)
            self.ir = sensobs['ir']
            self.threshold = 0.3
            
    def _update_flag(self):
        #Checks the urrent values of the ir sensor and checks if any of them are darker than threshold
        values = self.ir.get_value()
        for v in values:
            if v < self.threshold:
                self.active_flag = True
                return True
        self.active_flag=False
        return False
        
    def _sense_and_act(self):
        
        if self.active_flag:
            self.match_degree = 200
            self.motor_recommendation.action = "b" 
            self.motor_recommendation.description = 'WATCH OUT, THE WALL!!!!'
        
