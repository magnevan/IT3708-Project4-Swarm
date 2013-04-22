from layer import Layer
import time
import math
import random

BACKTRACK_AFTER_STAGNATION_FOR_MS = 2000
TIME_REQUIRED_FOR_STAGNATION = 2000
STAGNATION_PROXIMITY_THRESHOLD = 400

class StagnationLayer(Layer):
    stagnated_at = None
    previous_proximities = None

    def __init__(self):
        self.stagnated_at = 0
        self.previous_proximities = []

    def act(self, proximities, lights, acceleration, previous_layer_did_suppress):
        current_time = time.time() * 1000
        
        if self.stagnated_at + BACKTRACK_AFTER_STAGNATION_FOR_MS < current_time:
            print "Has not stagnated. ({0})".format(previous_layer_did_suppress)
            # Add the first two values of acceleration.
            if (not math.isnan(proximities[5]) and not math.isnan(proximities[6]) and
                not math.isnan(proximities[0]) and not math.isnan(proximities[1])):
                self.previous_proximities.append((proximities[5], proximities[6], proximities[0], proximities[1]))

            # See if we have data from 'TIME_REQUIRED_FOR_STAGNATION' ago and thus can determine whether or not we have stagnated.
            if self._has_enough_data_to_determine_stagnation(self.previous_proximities):
                # Stagnation is only a possible state if the previous layer did suppress.
                if previous_layer_did_suppress:
                    # Have we stagnated?
                    if self._has_stagnated(self.previous_proximities):
                        self.stagnated_at = current_time
                        self.previous_proximities = []

            self.previous_proximities = self.previous_proximities[-TIME_REQUIRED_FOR_STAGNATION / 100:]

            should_supress = False
            return (0, 0,), should_supress
        else:
            print "BACKTRACKING FROM STAGNATION!"
            should_supress = True
            return (- random.randint(0, 10) / 10.0, -1.0,), should_supress

    def _has_enough_data_to_determine_stagnation(self, proximities):
        return len(self.previous_proximities) >= TIME_REQUIRED_FOR_STAGNATION / 100

    def _has_stagnated(self, proximities):
        check_n_steps_back = TIME_REQUIRED_FOR_STAGNATION / 100
        last_n_proximities = proximities[-check_n_steps_back:]
        last_n_proximities = [map(lambda x: x[i], last_n_proximities) for i in range(4)]

        return (all(max(i_proximities) - min(i_proximities) < STAGNATION_PROXIMITY_THRESHOLD for i_proximities in last_n_proximities) and
                any(max(i_proximities) > 1000 for i_proximities in last_n_proximities))

"""
class Stagnation(object):
    IR_DIFF_THRESHOLD = 4
    DISTANCE_DIFF_THRESHOLD = 10
    REVERSE_LIMIT  =20
    TURN_LIMIT = 10
    FORWARD_LIMIT = 40
    NEIGHBOR_LIMIT = 300

    left_wheel_speed = 0
    right_wheel_speed = 0

    green_LED_state = False

    # States
    NEUTRAL, YES, NO = 'neutral', 'yes', 'no'
    has_recovered = False
    turn_left = NEUTRAL


    # Counters
    reverse_counter = 0
    turn_counter = 0
    forward_counter = 0
    twice = 0
    align_counter = 0


    '''
    Internal functions
    '''

    def flip():
        from random import getrandbits
        return getrandbits(1)

    def LED_blink():
        green_LED_state = not green_LED_state

    # oh god who wrote this
    def realign(distances):
        diff_front = abs(distances[0], distances[-1])

        triggered = map(lambda x: x < LOW_DIST_VALUE, distances)

        # Are we pushing straight? If not, maybe we should try. If we are, maybe we should
        # try pushing from another angle
        if diff_front > ALIGN_STRAIGHT_THRESHOLD: # We are not pushing straight
            #Let's push straight
            if triggered[0]:
                right_wheel_speed = -500
		left_wheel_speed = 500
	    elif triggered[7]:
                right_wheel_speed = 500
		left_wheel_speed = -500
	    elif triggered[1]:
                right_wheel_speed = -1000
		left_wheel_speed = 700
	    elif triggered[6]:
                right_wheel_speed = 700
		left_wheel_speed = -1000
	else: # We are not pushing straight
            left_wheel_speed = 500
            right_wheel_speed = -500
            if flip():
                left_wheel_speed, right_wheel_speed = right_wheel_speed, left_wheel_speed


        has_recovered = True
        green_LED_state = False





    '''
    External functions
    '''

    # This method is monsterous, blame the author who wrote the C code
    def find_new_spot(distances, DIST_THRESHOLD):
        if twice == 2: # Reverse, Turn, Forward, Turn(oposite), Forward
            has_recovered = True
            green_LED_state = False
        elif reverse_counter != REVERSE_LIMIT: # Make space by moving away from the box
            reverse_counter += 1
            left_wheel_speed = -800
            right_wheel_speed = -800
        elif turn_counter != TURN_LIMIT:
            turn_counter += 1
            forward_counter = 0

            if turn_left == NEUTRAL:
                turn_left = YES if flip() else NO

            left_wheel_speed = -300
            right_wheel_speed = 700

            if turn_left == NO:
                left_wheel_speed, right_wheel_speed = right_wheel_speed, left_wheel_speed

        elif forward_counter != FORWARD_LIMIT:
            forward_counter += 1
            if (forward_counter == FORWARD_LIMIT-1):
                twice += 1
                turn_counter = 0
                turn_left = NO if turn_left == YES else YES

            update_search_speed(distances, DIST_THRESHOLD)
            #TODO
            #left_wheel_speed = search.left_wheel_speed
            #right_wheel_speed = search_right_wheel_speed

            if min(left_wheel_speed, right_wheel_speed) > 0:
                left_wheel_speed = right_wheel_speed = 1000


    def reset_stagnation():
        has_recovered = FALSE
        reverse_counter = 0
        turn_counter = 0
        forward_coutner = 0
        turn_left = NEUTRAL
        twice = 0

    def stagnation_recovery(distances, DIST_THRESHOLD):
        if align_counter < 2:
            align_counter += 1
            realign(distances)
        elif align_counter > 0:
            LED_blink()
            find_new_spot(distances, DIST_THRESHOLD)

    # To keep pushing or not to keep pushing, that is the question
    def valuate_pushing(distances, prev_distances):
        diff = [abs(i - j) for i, j in zip(prev_distances, distances)]

        # We are moving
        # We trust our neighbors
        # We take a chance
        if min((diff[0], diff[7])) > DISTANCE_DIFF_THRESHOLD \
           or min((distances[5], distances[2])) > NEIGHBOR_LIMIT \
           or (max((distances[5], distances[2])) > NEIGHBOR_LIMIT and flip()):
            has_recovered = True # Keep pushing, it is working
            green_LED_state = False # No more recovery
            align_counter = 0


    # Return the boolean value of whether or not to continue with this layer
    def get_stagnation_state():
        return not has_recovered
"""
