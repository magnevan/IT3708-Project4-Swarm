from behavior import Behavior



class SearchBehavior(Behavior):
    def act(self, inputs):
        should_supress = False
        return (-.5, .5,), should_supress





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


