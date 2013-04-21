import random
import epuck_basic as epb
from search import SearchBehavior
from retrival import RetrivalBehavior
from stagnation import StagnationBehavior


class Botty(epb.EpuckBasic):
    def __init__(self):
        super(Botty, self).__init__()
        self.basic_setup()

        # XXX TODO s/Behavior/Layer in all files
        self._layers = [
            SearchBehavior(),
            RetrivalBehavior(),
            StagnationBehavior(),
        ]

    def run(self):
        while True:
            self._tick()

    def _tick(self):
        inputs = self.get_proximities()

        # Run all layers
        layer_actions = [layer.act(inputs) for layer in self._layers]

        # Chose output action
        output = None
        for proposed_output, should_supress in layer_actions:
            if output is None or should_supress:
                output = proposed_output

        self.move_wheels(*output)
        self._report_actions(layer_actions)

    def _report_actions(self, layer_actions):
        debug_str = '|'.join([
            '(%-.2f, %-.2f,)%s' % (
                left, right,
                'SUPRESS' if should_supress else '',
            )
            for (left, right,), should_supress in layer_actions
        ])
        print debug_str


if __name__ == '__main__':
    controller = Botty()
    controller.run()
