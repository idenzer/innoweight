import odrive

print("Configuring odrive")
odrv0 = odrive.find_any(timeout=10)
if str(odrv0) == "None":
    print("Didn't find an odrive :(")
else:
    print("Found an odrive!")
    print("Bus voltage is: ", str(odrv0.vbus_voltage))
odrv0.erase_configuration()
# set the limits
odrv0.axis0.motor.config.current_lim = 5 # [A]
odrv0.axis0.controller.config.vel_limit = 10 # [turns per second]
odrv0.axis0.motor.config.calibration_current = 10 # [A]
print("set the limits")


# set other hardware parameters
odrv0.config.brake_resistance = 0 # [ohm]
odrv0.axis0.motor.config.pole_pairs = 7 * (34/7) # times gear ratio to compensate for encoder
odrv0.axis0.motor.config.torque_constant = 8.27 / 140
#print(odrv0.axis0.motor.config.motor_type)
odrv0.axis0.encoder.config.cpr = 8192
print("set the hardware parameters")

odrv0.save_configuration() 


