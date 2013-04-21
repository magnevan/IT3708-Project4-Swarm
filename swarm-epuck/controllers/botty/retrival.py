from behavior import Behavior



class RetrivalBehavior(Behavior):
    def act(self, inputs):
        should_supress = False
        return (0, 0,), should_supress



class Retrival:
    PUSH_THRESHOLD = 500

    left_wheel_speed = 0
    right_wheel_speed = 0

    LED = [False]*8 #LED lights state

    '''
    Internal functions
    '''

    def update_speed(IR_number):
        cases = {0:(700,0),
                 1:(350,0),
                 2:(550,-300),
                 3:(500,0)}
        transf = [0,1,2,3,3,2,1,0]

        motors = cases[tranf[IR_number]]
        lp, rp = motors if IR_number < 4 else reversed(motors)

        left_wheel_speed += lp
        right_wheel_speed += rp

    # The movement for converging to the box
    def converge_to_box(IR_sensors, IR_threshold):
        left_wheel_speed = right_wheel_speed = 0

        LED = [False]*8
        for i, val in enumerate(IR_sensors):
            if val < IR_threshold:
                LED[i] = True
                update_speed(i)


    # The behavior when pushing the box
    def push_box(IR_sensors, IR_threshold):
        left_wheel_speed = right_wheel_speed = 0

        # Blink LED
        LED = [not l for l in LED]

        if IR_sensors[0] < IR_threshold and IR_sensors[7] < IR_threshold:
            left_wheel_speed = 1000
            right_wheel_speed = 1000
        else:
            # Update speeds for all triggering sensors
            (update_speed(i) for i,v in enumerate(IR_sensors) if v < IR_threshold)


    # Selects the behavior push or converge
    def select_behavior(IR_sensors):
        is_pushing = any(ir < PUSH_THRESHOLD for ir in IR_sensors)

    '''
    External functions
    '''

    # Converge, push, and stagnation recovery
    def swarm_retrival(IR_sensors, IR_threshold):
        select_behavior(IR_sensors)
        if select_behavior(IR_sensors):
            push_box(IR_sensors, IR_threshold)
        else:
            converge_to_box(IR_sensors, IR_threshold)
