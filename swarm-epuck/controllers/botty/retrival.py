import random
from layer import Layer


RETRIVAL_THRESHOLD =  1500
PUSH_THRESHOLD     =  3500



class RetrivalLayer(Layer):
    def act(self, proximities, lights, acceleration):
        lowest_intensity = min(lights)

        should_retrive = lowest_intensity <= RETRIVAL_THRESHOLD
        if not should_retrive:
            return (0, 0,), False

        should_push = all(lights[i] < PUSH_THRESHOLD for i in (6, 7, 0, 1,))

        if should_push:
            output = 1, 1
        else:
            output = .3, -.3

        return output, True
