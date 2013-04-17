import epuck_basic as epb

# The webann is a descendent of the webot "controller" class, and it has the ANN as an attribute.

class Botty(epb.EpuckBasic):

    def __init__(self):
        epb.EpuckBasic.__init__(self)
        self.basic_setup() # defined for EpuckBasic
    

#*** MAIN ***
# Webots expects a controller to be created and activated at the bottom of the controller file.

controller = Botty()
#controller.spin_cw(duration=20, speed=1)
controller.forward(duration=5)