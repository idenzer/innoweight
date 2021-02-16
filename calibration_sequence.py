import odrive

odrv0 = odrive.find_any(timeout=5)
if str(odrv0) == "None":
    print("Didn't find an odrive :(")
else:
    print("Found an odrive!")
    print("Bus voltage is: ", str(odrv0.vbus_voltage))


# DO NOT RUN THIS IF WE HAVENT CHANGED ANYTHING MECHANICALLY!!!!!!
# Only run this with minimal friction / connections to the motor
answer = input("Only run this if the motor is not calibrated and the motor has minimal frication / mechanical connections. Type \"Yes\" to continu\n>")

if answer != "Yes":
    print("Quitted")
    quit()

# 1) Motor calibration
odrv0.axis0.motor.config.pre_calibrated = False # Disregard any previous motor calibration
odrv0.axis0.requested_state = 4 # AXIS_STATE_MOTOR_CALIBRATION. Measure phase resistance and inductance

if odrv0.axis0.motor.is_calibrated:
    print("Motor calibration succeeded!")
else:
    print("Motor calibration failed!")
    quit()

odrv0.axis0.motor.config.pre_calibrated = True # No need to perform motor calibration in the future
odrv0.save_configuration() # Save motor calibration

# 2) Encoder index calibration
odrv0.axis0.encoder.config.pre_calibrated = False # Disregard any previous encoder calibration
odrv0.axis0.encoder.config.use_index = True # Use the encoder index in the future
odrv0.axis0.requested_state = 6 # AXIS_STATE_ENCODER_INDEX_SEARCH. Rotate motor until index pulse found

# 3) Encoder calibration
odrv0.axis0.requested_state = 7 # AXIS_STATE_ENCODER_OFFSET_CALIBRATION. 

if odrv0.axis0.encoder.is_ready:
    print("Motor calibration succeeded!")
else:
    print("Encoder calibration failed!")
    quit()

odrv0.axis0.encoder.config.pre_calibrated = True
odrv0.save_configuration()

# If sucessful we dont have to calibrate again! Use this code instead of the calibration at the beginning of the file
# odrv0.axis0.requested_state = 6 # AXIS_STATE_ENCODER_INDEX_SEARCH
# This still rotates the motor to find the index pulse, but only a tiny rotation. Also can do the search with anything attatched to the motor