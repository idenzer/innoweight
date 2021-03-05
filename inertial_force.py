import odrive
import time
import math

odrv0 = None

#conversions
lbs_to_kgs = 0.45359
inch_to_meter = 0.0254
#globals
g=9.8
stage_one_ratio = 4.8
stage_two_ratio = 6
gear_ratio = stage_one_ratio * stage_two_ratio
spool_diameter_inch = 6;
spool_diameter_meter = spool_diameter_inch * inch_to_meter
spool_radius_meter = spool_diameter_meter / 2
spool_circumference_inch = spool_diameter_inch * math.pi
spool_circumference_meter = spool_diameter_meter *math.pi
kt = 0.059
max_current_limit = 5 #be careful, this is scary


def main():
    global odrv0
    find_odrive()
    check_calibration()

    try:
        cancellation_token = odrive.utils.start_liveplotter(lambda: [axis0.motor.current_control.Iq_measured])
        pos_start = odrv0.axis0.encoder.pos_estimate #maybe make this its own function for setting the lowpoint
        #turning on the machine (make sure the cable is spooled to the correct point)
        desired_weight = input("Weight (lbs): ")
        input("Press Enter to begin...") # this actually is any key pressed not just enter.

        begin_weight(desired_weight)

        while True:
            current = calculate_current(desired_weight) #might need to add a constant to account for friction
            if current > max_current_limit:
                print("max current limit reached") #We should probably break here when we put a realistic current limit
                current = max_current_limit
            odrv0.axis0.motor.config.current_lim = current
            odrv0.axis0.controller.input_pos = pos_start #not sure if this needs to be called at every loop iteration
    except:
        print("ERROR: Exception reached")
        odrv0.axis0.requested_state = 1


def find_odrive():
    global odrv0
    print("Configuring odrive")
    odrv0 = odrive.find_any(timeout=10)
    if str(odrv0) == "None":
        print("Didn't find an odrive :(")
        quit()
    else:
        print("Found an odrive!")
        print("Bus voltage is: ", str(odrv0.vbus_voltage))

def check_calibration():
    global odrv0
    print("Checking calibration")
    if not odrv0.axis0.motor.is_calibrated:
        print("ERROR: Motor is not calibrated")
        quit()
    if not odrv0.axis0.encoder.is_ready:
        print("Encoder is not ready. Attempting to find index.")
        odrv0.axis0.requested_state = 6 # Find index pulse
        time.sleep(5)
        if not odrv0.axis0.encoder.is_ready:
            print("ERROR: Find index failed.")
            quit()
    print("Everything is calibrated")

def calculate_current(desired_weight, numMotors=1, use_acceleration=True):
    global odrv0
    
    kgweight = desired_weight * lbs_to_kgs
    a = read_acceleration() #need to calculate acceleration, for now it's 0 (constant force)
    if numMotors > 2:
        print("Invalid number of motors, failed to calculate current")
        return
    if use_acceleration == True:
        current = (kgweight*(a+g)*spool_radius_meter)/(gear_ratio*kt)
    else:
        current = (kgweight*(g)*spool_radius_meter)/(gear_ratio*kt)

    return current/numMotors

def read_acceleration():
    global odrv0
    vel_time_step = 0.1 #seconds
    motor_turn1 = odrv0.axis0.vel_estimate
    time.sleep(vel_time_step) # waits 0.1 seconds to get second velocity
    motor_turn2 = odrv0.axis0.vel_estimate
    travel_velocity1 = motor_turn1/stage_one_ratio/stage_two_ratio * spool_circumference_meter
    travel_velocity2 = motor_turn2/stage_one_ratio/stage_two_ratio * spool_circumference_meter
        
    return (travel_velocity2-travel_velocity1)/vel_time_step


def begin_weight(desired_weight):
    global odrv0
    print(desired_weight)
    odrv0.axis0.motor.config.current_lim = 10 # max current
    odrv0.axis0.motor.config.curren_lim_margin = 15
    odrv0.axis0.controller.config.control_mode = 3 # torque control
    odrv0.axis0.requested_state = 8 

    ramp_to_weight(desired_weight, 5)
    return

def ramp_to_weight(weight, time_to_weight):
    global odrv0
    target_current = calculate_current(desired_weight, use_acceleration=False)
    current = 0
    step_size = 0.05
    while (current < target_current and current < max_current_limit):
        current+=step_size
        odrv0.axis0.motor.config.current_lim = current
        odrv0.axis0.controller.input_pos = pos_start #not sure if this needs to be run at every loop, but if it does I gotta pass pos_start in or make global
        time.sleep(time_to_weight/(target_current/step_size))

    if current > target_current-0.1: #checks to see if you reached the intended weight or maxed out the current limit
        return True
    return False


if __name__ == '__main__':
    main()