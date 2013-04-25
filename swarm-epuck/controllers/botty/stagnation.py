from layer import Layer
import time
import math
import random

class StagnationLayer(Layer):
    def __init__(self):
        self._stagnation_rem = 0
        self._still_cnt = 0

    # OH YE LORDS OF THE UNIVERSE
    # BEHOLD THE UGLIEST CODE YOU HATH EVER SEEN
    def act(self, proximities, lights, speed, previous_layer_did_suppress):
        current_time = time.time()

        if self._stagnation_rem > 50:
            self._stagnation_rem -= 1
            return (-1, -random.uniform(0.5, 0.9),), True
        elif self._stagnation_rem > 40:
            self._stagnation_rem -= 1
            return random.choice([
                (1.0, -1),
                (-.5, 1)
            ]), True
        elif self._stagnation_rem > 0:
            self._stagnation_rem -= 1
            return (1,  1,), True

        if abs(speed[0]) < 1E-2 and abs(speed[1]) < 1E-2:
            self._still_cnt += 1
        else:
            self._still_cnt = 0

        if self._still_cnt >= 50 and random.random() < 0.1:
            self._stagnation_rem = 80
            self._still_cnt = 0

        return (0, 0,), False