import random
from behavior import Behavior


RETRIVAL_THRESHOLD =   200
PUSH_THRESHOLD     =  2000



class RetrivalBehavior(Behavior):
    """
    Currently just doing some random shit.
    """

    def __init__(self):
        super(RetrivalBehavior, self).__init__()
        self._t = random.randint(0, 20)

    def act(self, inputs):
        highest_intensity = max(inputs)

        should_retrive = highest_intensity >= RETRIVAL_THRESHOLD
        if not should_retrive:
            return (0, 0,), False

        print inputs

        #max_off_input = max(inputs[1:])
        should_push = (inputs[0] >= PUSH_THRESHOLD and
                       inputs[1] >= PUSH_THRESHOLD)

        if should_push:
            output = 1, 1
        else:
            output = .5, 0

        return output, True
