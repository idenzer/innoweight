import odrive
import time
#conversions
lbs_to_kgs = 0.45359
inch_to_meter = 0.0254
#globals
g=9.8
stage_one_ratio = 4.8
stage_two_ratio = 7
gear_ratio = stage_one_ratio * stage_two_ratio
spool_diameter_inch = 6;
spool_diameter_meter = spool_diameter_inch * inch_to_meter
spool_radius_meter = spool_diameter_meter/2
kt = 0.059
max_current_limit = 5 #be careful, this is scary

"""
"""
if __name__ = __main__:
	main()
"""
"""


def main:
	find_odrive()

	cancellation_token = start_liveplotter(lambda: [axis0.motor.current_control.Iq_measured])
	pos_start = odrv0.axis0.encoder.pos_estimate #maybe make this its own function for setting the lowpoint
	#turning on the machine (make sure the cable is spooled to the correct point)
	desired_weight = input("Weight (lbs): ")
	input("Press Enter to begin...")

	begin_weight(desired_weight)

	while True:
		current = calculate_current(desired_weight) #might need to add a constant to account for friction
		if current > max_current_limit:
			print("max current limit reached") #We should probably break here when we put a realistic current limit
			current = max_current_limit
		odrv0.axis0.motor.config.current_lim = current
		odrv0.axis0.controller.input_pos = pos_start #not sure if this needs to be called at every loop iteration


def find_odrive():
	print("Configuring odrive")
	odrv0 = odrive.find_any(timeout=10)
	if str(odrv0) == "None":
    	print("Didn't find an odrive :(")
	else:
    	print("Found an odrive!")
    	print("Bus voltage is: ", str(odrv0.vbus_voltage))

def calculate_current(desired_weight, numMotors=1, use_acceleration=True):
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
	return 0

def begin_weight(desired_weight):

	odrv0.axis0.motor.config.current_lim = 0.1
    odrv0.axis0.controller.config.control_mode = 3 # position control
    odrv0.axis0.requested_state = 8 

    ramp_to_weight(desired_weight, 5)
    return

def ramp_to_weight(weight, time_to_weight):
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
