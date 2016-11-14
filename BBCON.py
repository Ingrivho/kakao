# import modules here

__author__ = 'estensen'


class Bbcon:
    def __init__(self, behaviors, sensobs, motob, arbitrator):
        """Initialize bbcon.

        Parameters
        ----------
        behaviors : A list of all the behavior objects used by the bbcon.
        active_behaviors : A list of all behaviors that are currently active.
        sensobs : A list of all sensory objects used by the bbcon.
        motobs : A list of all motor objects used by the bbcon.
        arbitrator : The arbitrator object that will resolve actuator requests produced by the behaviors.
        timestep : Global clock.
        """
        self.behaviors = behaviors
        self.sensobs = sensobs
        self.motob = motob
        self.arbitrator = arbitrator
        self.timestep = 0
        self.motor_recommendation = ('F', 1)  # Initial motor recommendation is forward, 1 second.

    def add_behavior(self, new_behavior):
        """Append a newly-created behavior onto the behaviors list."""
        self.behaviors.add(new_behavior)

    def add_sensob(self, new_sensob):
        """Append a newly-created sensob onto the sensobs list."""
        self.sensobs.add(new_sensob)

    def run_one_timestep(self):
        """Constitutes core activity."""
        # print("Updating sensobs...")
        # Update all sensobs.
        # These updates will involve querying the relevant sensors for their values,
        # along with any pre-processing of those values (as described below)
        for sensob in self.sensobs:
            sensob.update()
        # print("Sensobs updated.")

        # print("Updating behaviors...")
        for behavior in self.behaviors:
            behavior.sense_and_act()
        # These updates involve reading relevant sensob values and producing a motor recommendation.
        # print("Behaviors updated.")

        # print("Calling arbitrator...")
        self.motor_recommendation = self.arbitrator.choose_action(self.behaviors)
        # print('Got a motor recommendation from the arbitrator')

        # print("Updating motob with motor recommendations...")
        # The motobs will then update the settings of all motors.
        self.motob.update(self.motor_recommendation)
        self.timestep += 1

        # print("One timestep finished")
