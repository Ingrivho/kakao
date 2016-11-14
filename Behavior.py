from motor_rec import Motor_Rec

class Behavior():
    # constructor that takes in the bbcon this Behavior is reporting to, what sensors it uses,
    # if it is currently active, and a static priority. 
    def __init__(self, sensobs, active_flag, static_priority):
        self.sensobs = sensobs
        self.active_flag = active_flag
        # static_priority is a static, final varibale. It should not be changed after init. Dont know how to do this in python
        self.static_priority = static_priority
        #creates an empty motor rec, this will not be returned unless its been alternated. 
        self.motor_recommendation = Motor_Rec(0, None)
        self.match_degree = 0

        # Below are some effectivley abstract classes. Each subclass of Behavior have to define these functions themselves. 
    def _update_flag(self):
     	# REMEMBER TO DO THIS
        raise Exception('_update_flag was not implemented in class Behavior')
    def _sense_and_act(self):
        #This is the main function of the Behavoir class. This function should:
        #1 get an update from all sensobs in its sensob list self.sensob
        #2 make a decision based on the sensor inputs
        #3 update self.motor_recommandations and self.match_degree based on the decision
        raise Exception('_sense_and_act was not implemented in class Behavior')
        return

    def get_update(self):
        #Do not implement this function yourself. Use sense_and_act, and let get update do the rest
        self._update_flag()
        self._sense_and_act()
        self.weight = self.static_priority * self.match_degree
        self.motor_recommendation.pri = self.weight
        return (self.motor_recommendation)
