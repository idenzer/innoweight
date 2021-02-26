
import odrive

print("Configuring odrive")
odrv0 = odrive.find_any(timeout=10)
if str(odrv0) == "None":
    print("Didn't find an odrive :(")
else:
    print("Found an odrive!")
    print("Bus voltage is: ", str(odrv0.vbus_voltage))

# set the limits
odrv0.axis0.motor.config.current_lim = 5 # [A]
odrv0.axis0.motor.config.current_lim_margin = 15
odrv0.axis0.controller.config.vel_limit = 50 # [turns per second]
odrv0.axis0.motor.config.calibration_current = 10 # [A]
print("set the limits")

# set other hardware parameters
odrv0.config.brake_resistance = 2 # [ohm]
odrv0.axis0.motor.config.pole_pairs = 7 # times gear ratio to compensate for encoder
odrv0.axis0.motor.config.torque_constant = 1 #8.27 / 140. control via amps instead of torque
#print(odrv0.axis0.motor.config.motor_type)
odrv0.axis0.encoder.config.cpr = 8192
print("set the hardware parameters")

#current control velocity limit 10


odrv0.save_configuration() 