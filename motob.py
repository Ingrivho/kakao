from motors import Motors

__author__ = 'estensen'


class Motob:
    """Interface between a behavior and one or more motors."""
    def __init__(self):
        """Initialize Motob object.

        Parameters
        ----------
        action : Holder of the action whose settings will be determined by the motob.
        duration : Holder of the most recent duration the of the action.
        """
        self.m = Motors()
        self.action = None
        self.duration = None

    def update(self, recommendation):
        # print('Motor recommendation:', recommendation)
        """Update object.

        Receive a new motor recommendation.
        Load it into the instance variables.
        Operationalize it.

        Example
        -------
        recommendation = ('L', 1)
        """
        self.m.stop()
        self.action = recommendation[0]
        self.duration = recommendation[1]
        self.operationalize(self.action, self.duration)

    def operationalize(self, action, duration):
        """Convert motor recommendation into motor setting and send to corresponding motor(s).

        Parameters
        ----------
        action : Action the motors will perform.
        dur : Duration of the operation.

        Example of actions
        ------------------
        F = Drive forward
        B = Drive backward
        Z = Boost forward
        X = Flee
        T = Turn around 180 degrees
        L = Turn left while driving forward
        R = Turn right while driving forward
        S = Stop
        """
        if action == 'F':
            self.m.set_value((0.5, 0.5), duration)
        elif action == 'B':
            self.m.backward(0.25, duration)
        elif action == 'Z':
            self.m.set_value((1, 1), duration)
        elif action == 'X':
            self.m.flee()  # Turn around, must be tuned for 180 degree turn.
        elif action == 'T':
            self.m.turn()
        elif action == 'L':
            self.m.left((0.1, 0.25), duration)
        elif action == 'R':
            self.m.right((0.25, 0.1), duration)
        elif action == 'S':
            self.m.stop()
