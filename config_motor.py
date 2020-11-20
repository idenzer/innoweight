import odrive

print("Configuring odrive")

odrv0 = odrive.find_any(timeout=5)
if str(odrv0) == "None":
    print("Didn't find an odrive :(")
else:
    print("Found an odrive!")
    print("Bus voltage is: ", str(odrv0.vbus_voltage))

# set the limits
odrv0.axis0.motor.config.current_lim = 5 # [A]
odrv0.axis0.controller.config.vel_limit = 10 # [turns per second]
odrv0.axis0.motor.config.calibration_current = 3 # [A]
print("set the limits")

# set other hardware parameters
odrv0.config.brake_resistance = 0 # [ohm]
odrv0.axis0.motor.config.pole_pairs = 7 * 5 # times 5 to compensate for encoder
odrv0.axis0.motor.config.torque_constant = 8.27 / 140
odrv0.axis0.motor.config.motor_type = 
print("set the hardware parameters")


odrv0.save_configuration() 


<odrv>.<axis>.motor.config.current_lim = <Float>