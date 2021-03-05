import odrive
import time
import math


def main():
    odrv0 = odrive.find_any(timeout=5)
    if str(odrv0) == "None":
        print("Didn't find an odrive :(")
        quit()
    else:
        print("Found an odrive!")
        print("Bus voltage is: ", str(odrv0.vbus_voltage))

    if not odrv0.axis0.motor.is_calibrated:
        print("Motor not calibrated!")
        quit()
    if not odrv0.axis0.encoder.is_ready:
        print("Encoder not ready!")
        quit()

    print("start pos: ", odrv0.axis0.encoder.pos_estimate)

    odrv0.axis0.controller.config.control_mode = 2 # velocity control
    odrv0.axis0.requested_state = 8

    odrv0.axis0.controller.input_vel = 1.5
    odrv0.axis0.motor.config.current_lim = 10

    t = time.time()
    while (time.time() - t < 5) and abs(odrv0.axis0.motor.current_control.Iq_measured) < 5:
        print(odrv0.axis0.motor.current_control.Iq_measured)
    odrv0.axis0.controller.input_vel = 0
    pos_right = odrv0.axis0.encoder.pos_estimate

    odrv0.axis0.requested_state = 1
    print("Exited program.")
    quit()

if __name__ == '__main__':
    main()