import time
import math
import threading
import random
import epuck_basic as epb
from search import SearchLayer
from retrival import RetrivalLayer
from stagnation import StagnationLayer


class AccelerationSamplingThread(threading.Thread):
    def __init__(self, epuck):
        super(AccelerationSamplingThread, self).__init__()
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

    def get_speed(self):
        with self._lock:
            last = self._last[:]

        if not last:
            return (42, 42,)

        v_xs = []
        v_ys = []

        for (t0, (a0x, a0y,),), (t1, (a1x, a1y,),) in zip(last, last[1:]):
            dt = t1 - t0
            v_x = (a1x - a0x) / dt
            v_y = (a1y - a0y) / dt
            v_xs.append(v_x)
            v_ys.append(v_y)


        v_x_mean = sum(v_xs) / len(v_xs)
        v_y_mean = sum(v_ys) / len(v_ys)

        return (v_x_mean, v_y_mean,)


class Botty(epb.EpuckBasic):
    def __init__(self):
        super(Botty, self).__init__()
        self.basic_setup()

        self._layers = [
            SearchLayer(),
            RetrivalLayer(),
            StagnationLayer(),
        ]

        self._acc_sampler = AccelerationSamplingThread(self)
        self._acc_sampler.start()

    def run(self):
        while True:
            self._tick()

    def _tick(self):
        proximities = self.get_proximities()
        lights = self.get_lights()
        acceleration = self.get_accelleration()

        layer_actions = []

        speed = self._acc_sampler.get_speed()

        # Run all layers
        for layer in self._layers:
            layer_actions.append(layer.act(
                proximities,
                lights,
                speed,
                layer_actions[-1][1] if len(layer_actions) > 0 else None))

        # Chose output action
        output = None
        for proposed_output, should_supress in layer_actions:
            if output is None or should_supress:
                output = proposed_output

        self.move_wheels(*output)
        self._report(layer_actions, speed)

    def _report(self, layer_actions, speed):
        debug_str = '    '.join([
            '[%-8.2f %-8.2f %-7s]' % (
                left, right,
                'SUPRESS' if should_supress else '',
            )
            for (left, right,), should_supress in layer_actions
        ])
        debug_str += ' (%.2f %.2f) ' % speed
        print debug_str


if __name__ == '__main__':
    controller = Botty()
    controller.run()
