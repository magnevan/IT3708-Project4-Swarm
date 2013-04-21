import random
import epuck_basic as epb
from search import SearchBehavior
from retrival import RetrivalBehavior
from stagnation import StagnationBehavior


R = random.Random(0x42)


class Botty(epb.EpuckBasic):
    def __init__(self):
        super(Botty, self).__init__()
        self.basic_setup()

        self._behaviors = (
            SearchBehavior(),
            RetrivalBehavior(),
            StagnationBehavior(),
        )

    def run(self):
        while True:
            self._tick()

    def _tick(self):
        inputs = get_proximities()

        output = None
        for b in self._behaviors:
            proposed_output, should_supress = b.act(inputs)
            if output is None or should_supress:
                output = proposed_output

        self.move_wheels(*output)


if __name__ == '__main__':
    controller = Botty()
    controller.run()
