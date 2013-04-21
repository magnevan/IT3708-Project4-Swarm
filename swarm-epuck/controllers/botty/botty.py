import random
import epuck_basic as epb
from search import SearchLayer
from retrival import RetrivalLayer
from stagnation import StagnationLayer


class Botty(epb.EpuckBasic):
    def __init__(self):
        super(Botty, self).__init__()
        self.basic_setup()

        self._layers = [
            SearchLayer(),
            RetrivalLayer(),
            StagnationLayer(),
        ]

    def run(self):
        while True:
            self._tick()

    def _tick(self):
        proximities = self.get_proximities()
        lights = self.get_lights()
        acceleration = self.get_accelleration()

        # Run all layers
        layer_actions = [layer.act(proximities, lights, acceleration)
                         for layer in self._layers]

        # Chose output action
        output = None
        for proposed_output, should_supress in layer_actions:
            if output is None or should_supress:
                output = proposed_output

        self.move_wheels(*output)
        self._report_actions(layer_actions)

    def _report_actions(self, layer_actions):
        debug_str = '    '.join([
            '[%-8.2f %-8.2f %-7s]' % (
                left, right,
                'SUPRESS' if should_supress else '',
            )
            for (left, right,), should_supress in layer_actions
        ])
        print debug_str


if __name__ == '__main__':
    controller = Botty()
    controller.run()
