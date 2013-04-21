from behavior import Behavior
import random
R = random.Random(0x42)

# How close we need to be before we consider it noticable
DIST_THRESH = 10

# How quickly we allow the speed to change
SP_CHANGE = 0.05

class SearchBehavior(Behavior):
    motor = [R.uniform(.5,1.0), R.uniform(.5,1.0)]
       
    def find_speed(self, inputs):
        # Random walk
        if R.random() < 0.01:
            self.motor = (-1,1) if R.getrandbits(1) else (1,-1)
        else:
            self.motor = [R.uniform(.5,1.0), R.uniform(.5,1.0)]
        
        return self.motor
            
    def act(self, inputs):
        should_supress = False
        return self.find_speed(inputs), should_supress

"""
class Search(object):
    COUNTLIMIT = 20
    counter = COUNTLIMIT

    left_wheel_speed = 0
    right_wheel_speed = 0

    # Random search speed
    rand_double_left = 0
    rand_double_right = 0

    # Case scenarios for navigation, key is sensor input, val is motor out
    cases = {(0,0,0,0):(1,1),
             (0,0,0,1):(1,0),
             (0,0,1,0):(1,0),
             (0,0,1,1):(1,0),
             (0,1,0,0):(0,1),
             (0,1,0,1):(1,0),
             (0,1,1,0):(0,1),
             (0,1,1,1):(1,0),
             (1,0,0,0):(0,1),
             (1,0,0,1):(1,0),
             (1,0,1,0):(0,1),
             (1,0,1,1):(1,0),
             (1,1,0,0):(0,1),
             (1,1,0,1):(1,0),
             (1,1,1,0):(0,1),
             (1,1,1,1):(0,1)}

    '''
    Internal functions
    '''

    def randdouble():
        from random import random
        rand_double_left = random()
        rand_double_right = random()

    # Given the input compared to the case script; where do we want to go?
    def calculate_search_speed(threshold_list):
        counter += 1

        motor = cases[threshold_list]
        if counter >= COUNTLIMIT:
            counter = 0
            randdouble()

        if motor == (1,1): # Free passage; straight forward
            left_wheel_speed = rand_double_left*500 + 500
            right_wheel_speed = rand_double_right*500 + 500
        elif motor == (1,0):
            left_wheel_speed = -300
            right_wheel_speed = 700
        elif motor == (0,1):
            left_wheel_speed = 700
            right_wheel_speed = -300


    # Calculate if there is an obstacle or not, depending on the threshold
    def calculate_treshold(sensors, distance_threshold):
        threshold_list = map(lambda x: x < distance_threshold, sensors)
        calculate_search_speed(threshold_list)

    '''
    External functions
    '''

    # Given the sensor input and threshold, calculates the speed for survival
    def update_search_speed(sensor_value, distance_threshold):
        sv = sensor_value
        calculate_threshold([sv[6], sv[7], sv[0], sv[1]], distance_threshold)

"""