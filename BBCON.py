from time import sleep
from ultrasonic import *
from Arbitrator import Arbitrator
from reflectance_sensors import ReflectanceSensors
from camera import Camera
from derp import Derp
from motors import Motors
from driveToColor import driveToColor
from watchOutForTheWall import WatchOutForTheWall
from turnAtEdge import TurnAtEdge
from zumo_button import ZumoButton

class BBCON():

    def __init__(self, behaviors, sensobs):
        #init instance variables from input.
        self.behaviors = set(behaviors)
        self.sensobs = sensobs # Dictionary of sensobject, 'camera' -> camera sensobj
        self.camera_count = -1
        self.arbitrator = Arbitrator()
        self.motors = Motors()

    def _update_sensobs(self):
        # Increment the camera_count variable each time we check our sensors
        self.camera_count += 1
        self.camera_count = self.camera_count % 10

        for ob in self.sensobs:
            if ob != 'camera':
              self.sensobs[ob].update()

            elif self.camera_count == 0:
              print('Smile for the camera!')
              # Only use the camera if the camera_counter is equal to zero
              self.motors.stop()
              self.sensobs[ob].update()

    def _update_behaviors(self):

        for behavior in self.behaviors:

          if behavior.__class__.__name__ != 'driveToColor':
            mr = behavior.get_update() # Get our beloved motor recommendation from the behavior


          elif self.camera_count == 0:
            # This elif will only trigger if the behaviour name is driveToColor
            # Only execute if the camera_count is equal to zero
            # This lets ut skip image processing if the picture isnt taken this iteration

            mr = behavior.get_update() # Get our beloved motor recommendation from the behavior
            print('Process camera image')

          if behavior.active_flag: # If it is active, we add it to the arbitrator for further evaluation :3
            self.arbitrator.add_mr(mr)
            behavior.active_flag = False


    def loop(self):
      self._update_sensobs() # Update all sensors
      self._update_behaviors() # Use the information to generate motor recommendations
      mr = self.arbitrator.choose_action() # Let the great arbitrator decide what to do based on the recommendations
      self.motors.do(mr.action) # COMPLETE THE CYCLE
      sleep(0.01) # Sleep a little bit.. What happens if we remove this?


# Initialize all our senobs
button = ZumoButton();
rs = ReflectanceSensors()
camera = Camera()
ultra = Ultrasonic()

# Put these into a sexy dictionary
sensobs = {'ir' : rs,  'ultrasonic' : ultra, 'camera' : camera }

# Intialize and add behaviors to our list
behaviors = [];

behaviors.append(WatchOutForTheWall(sensobs, 5));
behaviors.append(TurnAtEdge(sensobs, 5));
behaviors.append(driveToColor(sensobs, 8))

# Initialize behavior based controller
bbcon = BBCON(behaviors, sensobs)

# Motor stuff
bbcon.motors.setMax(200);
bbcon.motors.setTurnSpeed(400);
bbcon.motors.setTurnDur(4); #bør være rundt 12

print("max speed:" + str(bbcon.motors.max));
print("waiting for press...");
print("beginning opening ritual with 180 degree turns");

button.wait_for_press();
sleep(2);

bbcon.motors.turnAround("r",180);
bbcon.motors.turnAround("l",180);

while True and button.button_pressed(): # button_pressed actually means button not pressed
  bbcon.loop()

bbcon.motors.stop(); # STOP MOVING PLZ
