
from motor_rec import Motor_Rec

class Arbitrator():
    def __init__(self):
        self.forward_rec = Motor_Rec(1,1, 'Default, drive forward');
        self.motor_recs = [self.forward_rec] #instansiates a min queue of motor_recommendations

    def add_mr(self, motor_rec):

        self.motor_recs.append(motor_rec)

    def choose_action(self):
        #gets the motor_rec with highest priority, returns it and empties the queueue 
        val = max(self.motor_recs)

        print('Motor recommendations received by the arbitrator: ')
        formatted = map(lambda mr: ('Decsript: %s \t Pri: %d \t Action: %r' % (mr.description, mr.pri, mr.action)), self.motor_recs)
        for string in formatted:
          print(string)
        print('The arbitrator chose the one with the hightest priority: %s' % val.description)
        print('---')

        self.motor_recs = [self.forward_rec];
        return val
