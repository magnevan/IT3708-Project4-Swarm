from layer import Layer
import random
R = random.Random()

# How close we need to be before we consider it noticable
DIST_THRESH = 1000

class SearchLayer(Layer):
    motor = [R.uniform(.5,1.0), R.uniform(.5,1.0)]
    
    # ticks to change [speed]
    ttc = R.randint(5,40)

    def find_speed(self, proximities):
        right, left = proximities[:3], proximities[5:]
    
        # Check for walls
        if any(p > DIST_THRESH for p in right+left):
            tot = sum(right+left)
            return (float(sum(left))/tot, float(sum(right))/tot)
        else:
            if not self.ttc:
                self.ttc = R.randint(5,40)
                self.motor = (R.uniform(.5,1.0), R.uniform(.5,1.0))
            
            self.ttc -= 1
            return self.motor

    def act(self, proximities, lights, acceleration, previous_layer_did_suppress):
        should_supress = False
        return self.find_speed(), should_supress
