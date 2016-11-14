from Behavior import *

class b_hunger(Behavior):
    def __init__(self, bbcon):
        #Init hunger with the bbcon it takes in, no sensors, not active and with a high static priority = 10
        super(self, bbcon, None, False, 10).__init__()
        #Introduce a hunger level. The higher the hunger level, the more satisfied we are. 
        #If the hunger_level is below 50, we are hungry. 
        self.hunger_level = 70

    def _update_flag(self):
        this.active_flag = not this.active_flag

    def _sense_and_act(self):
        #This is where we would check if the behavior is hungry, and look for the food source
        #we could say 'self.match_degree = self.hunger_level // 10, for example, and then request 
        #that we go to source. Loads of possibilities here, but since we havent got any working sensormodules yet, Ill let it be. 
        pass

    def get_update(self):
        #reduce the hunger_level every time the Behavior is asked for an update to simulate hunger.
        self.hunger_level -= 0.001
        super(self).get_update()
