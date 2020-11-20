import odrive

odrv0 = odrive.find_any(timeout=5)
if str(odrv0) == "None":
    print("Didn't find an odrive :(")
else:
    print("Found an odrive!")
    print("Bus voltage is: ", str(odrv0.vbus_voltage))

odrv0.axis0.requested_state = 3