import odrive

print("Configuring odrive")
odrv0 = odrive.find_any(timeout=10)
if str(odrv0) == "None":
    print("Didn't find an odrive :(")
else:
    print("Found an odrive!")
    print("Bus voltage is: ", str(odrv0.vbus_voltage))

print("Current Limit is: ", str(odrv0.axis0.motor.config.current_lim))
print("Velocity Limit is: ", str(odrv0.axis0.controller.config.vel_limit))
print("Control mode is: ", str(odrv0.axis0.current_state))

odrv0.axis0.requested_state = input("What control mode would you like: ")

odrv0.axis0.contorller.input_vel = input("What velocity limit [turns/s] would you like: ")