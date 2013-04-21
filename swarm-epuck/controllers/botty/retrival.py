import random
from behavior import Behavior


RETRIVAL_THRESHOLD =  1500
PUSH_THRESHOLD     =  3500



class RetrivalBehavior(Behavior):
    """
    Currently just doing some random shit.
    """

    def __init__(self):
        super(RetrivalBehavior, self).__init__()

    def act(self, inputs):
        lowest_intensity = min(inputs)

        should_retrive = lowest_intensity <= RETRIVAL_THRESHOLD
        if not should_retrive:
            return (0, 0,), False

        should_push = all(inputs[i] < PUSH_THRESHOLD for i in (6, 7, 0, 1,))

        if should_push:
            output = 1, 1
        else:
            output = .3, -.3

        return output, True
