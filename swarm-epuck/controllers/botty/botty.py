import time
import math
import threading
import random
import epuck_basic as epb
from search import SearchLayer
from retrieval import RetrivalLayer
from stagnation import StagnationLayer


class JoltSamplingThread(threading.Thread):
    def __init__(self, epuck):
        super(JoltSamplingThread, self).__init__()
        self._epuck = epuck
        self._lock = threading.Lock()
        self._keep_len = 10
        self._last = []

    def run(self):
        tpre = time.time()
        temp_last = []
        n = 0
        while True:
            time.sleep(0.01)

            ax, ay, _ = self._epuck.get_accelleration()
            if math.isnan(ax) or math.isnan(ay):
                continue

            temp_last.append( (time.time(), (ax, ay,)) )

            if len(temp_last) == self._keep_len:
                with self._lock:
                    self._last = temp_last[:]
                    temp_last = []

    def get_jolt(self):
        with self._lock:
            last = self._last[:]

        if not last:
            return (42, 42,)

        j_xs = []
        j_ys = []

        for (t0, (a0x, a0y,),), (t1, (a1x, a1y,),) in zip(last, last[1:]):
            dt = t1 - t0
            j_x = (a1x - a0x) / dt
            j_y = (a1y - a0y) / dt
            j_xs.append(j_x)
            j_ys.append(j_y)


        j_x_mean = sum(j_xs) / len(j_xs)
        j_y_mean = sum(j_ys) / len(j_ys)

        return (j_x_mean, j_y_mean,)


class Botty(epb.EpuckBasic):
    def __init__(self):
        super(Botty, self).__init__()
        self.basic_setup()

        self._layers = [
            SearchLayer(),
            RetrivalLayer(),
            StagnationLayer(),
        ]

        self._jolt_sampler = JoltSamplingThread(self)
        self._jolt_sampler.start()

    def run(self):
        while True:
            self._tick()

    def _tick(self):
        proximities = self.get_proximities()
        lights      = self.get_lights()
        jolt        = self._jolt_sampler.get_jolt()

        # Chose output action
        output = None
        for layer in self._layers:
            proposed_output, should_suppress = layer.act(proximities,
                                                        lights, jolt)

            if output is None or should_suppress:
                output = proposed_output

        self.move_wheels(*output)


if __name__ == '__main__':
    controller = Botty()
    controller.run()
