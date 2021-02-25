import odrive


global spool_width
print("Configuring odrive")
odrv0 = odrive.find_any(timeout=10)
if str(odrv0) == "None":
    print("Didn't find an odrive :(")
else:
    print("Found an odrive!")
    print("Bus voltage is: ", str(odrv0.vbus_voltage))

g=9.8
gear_ratio = 4.8
spool_diameter = .1524/2 #.127 if 5in can't remember
spool_radius = spool_diameter/2
kt = 0.059

cancellation_token = start_liveplotter(lambda: [axis0.motor.current_control.Iq_measured])

desired_weight = 100
while True:
	calculateCurrent(desired_weight)


def calculateCurrent(desired_weight, numMotors=1):
	#this should get moved to a different function
	lbs_to_kgs = 0.45359
	kgweight = desired_weight * lbs_to_kgs
	a = read_acceleration()
	if numMotors > 2:
		print("Invalid number of motors, failed to calculate current")
		return;

	current = (kgweight*(a+g)*spool_radius)/(gear_ratio*kt)
	if numMotors == 2:
		return current/2

	return current

def read_acceleration():
	return 0;
