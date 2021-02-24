import odrive

print("Configuring odrive")
odrv0 = odrive.find_any(timeout=10)
if str(odrv0) == "None":
    print("Didn't find an odrive :(")
else:
    print("Found an odrive!")
    print("Bus voltage is: ", str(odrv0.vbus_voltage))

g=9.8
first_reduction = 4.8
spool_width = .1524/2 #.127 if 5in can't remember

"""
We need to use threading to plot and run at the same time
I ain't setting that up rn
cancellation_token = start_liveplotter(axis0.motor.current_control.Iq_measured)
"""
while True:
	
	#some acceleration that is to be read in depending on how we implement it
	accel = 1

	#user input weight
	desired_weight = 100

	force = desired_weight*g + desired_weight*g*accel

	spool_torque = force/spool_width

	motor_torque = spool_torque/first_reduction

	current = motor_torque/kv

	odrv0.axis0.motor.config.current_lim = current