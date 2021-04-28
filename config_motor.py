
import odrive

print("Configuring odrive")
odrv0 = odrive.find_any(timeout=10)
if str(odrv0) == "None":
    print("Didn't find an odrive :(")
    quit()
else:
    print("Found an odrive!")
    print("Bus voltage is: ", str(odrv0.vbus_voltage))


#############################################################################################################
odrv0.config.brake_resistance = 1.3 # [ohm]
odrv0.config.max_regen_current = 0

#############################################################################################################

# set the limits
odrv0.axis0.motor.config.current_lim = 20 # [A]
odrv0.axis0.motor.config.current_lim_margin = 15
odrv0.axis0.controller.config.vel_limit = 50 # [turns per second]
odrv0.axis0.motor.config.calibration_current = 5 # [A]
# set other hardware parameters
odrv0.axis0.motor.config.pole_pairs = 7 
odrv0.axis0.motor.config.torque_constant = 8.27 / 140 #control via amps instead of torque
odrv0.axis0.motor.config.motor_type = 0 # high current type motor
odrv0.axis0.encoder.config.use_index=True
odrv0.axis0.encoder.config.cpr = 8192
odrv0.axis0.encoder.config.pre_calibrated = True
odrv0.axis0.motor.config.pre_calibrated = True
#current control velocity limit
odrv0.axis0.config.calibration_lockin.vel = -40
odrv0.axis0.config.calibration_lockin.accel = -20
odrv0.axis0.config.calibration_lockin.ramp_distance = -3.14159

#####################################################################################################################

odrv0.axis1.motor.config.current_lim = 20 # [A]
odrv0.axis1.motor.config.current_lim_margin = 15
odrv0.axis1.controller.config.vel_limit = 50 # [turns per second]
odrv0.axis1.motor.config.calibration_current = 5 # [A]
# set other hardware parameters
odrv0.axis1.motor.config.pole_pairs = 7 
odrv0.axis1.motor.config.torque_constant = 8.27 / 140 #control via amps instead of torque
odrv0.axis1.motor.config.motor_type = 0 # high current type motor
odrv0.axis1.encoder.config.use_index=True
odrv0.axis1.encoder.config.cpr = 8192
odrv0.axis1.encoder.config.pre_calibrated = True
odrv0.axis1.motor.config.pre_calibrated = True
#current control velocity limit 10
odrv0.axis1.config.calibration_lockin.vel = -40
odrv0.axis1.config.calibration_lockin.accel = -20
odrv0.axis1.config.calibration_lockin.ramp_distance = -3.14159

odrv0.save_configuration() 