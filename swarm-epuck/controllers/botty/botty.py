import random
import epuck_basic as epb
from search import Search
from retrival import Retrival
from stagnation import Stagnation

R = random.Random(0x42)

class Botty(epb.EpuckBasic):
    def __init__(self):
        epb.EpuckBasic.__init__(self)
        self.basic_setup() # defined for EpuckBasic

    def run(self):
        while True:
            R.choice([
                self.turn_left,
                self.turn_right,
            ])()
            print 'Proximities', self.get_proximities()

controller = Botty()
controller.run()
