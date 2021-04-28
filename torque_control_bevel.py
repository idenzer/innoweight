import odrive
import time
from odrive.utils import *

Kt = 8.27/150
deadband = 0.5 # [turns]
target_weight = 10 # [lb]
weight_to_torque = 46.8 # [lb / N]
target_torque = target_weight / weight_to_torque
min_torque = 0 # [Nm]

def current_to_torque(current):
    return (current * Kt)

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
        odrv0.axis0.requested_state = 6
        time.sleep(3)

    odrv0.axis0.controller.config.control_mode = 1 # torque control
    odrv0.axis0.requested_state = 8 # closed loop control
    pos_init = odrv0.axis0.encoder.pos_estimate
    slope_torque = min_torque + (target_torque - min_torque) / deadband

    while True:
        try:
            pos_curr = odrv0.axis0.encoder.pos_estimate
            pos_error = -1* (pos_curr - pos_init)
            if pos_error < 0:
                odrv0.axis0.controller.input_torque = 0
            elif pos_error < deadband:
                odrv0.axis0.controller.input_torque = pos_error * slope_torque
            else:
                odrv0.axis0.controller.input_torque = target_torque
            print("Pos_error: %.2f turns. Input torque: %.2f Nm" % (pos_error, odrv0.axis0.controller.input_torque))
        except:
            print("Exited program. Dumping errors.")
            dump_errors(odrv0)
            odrv0.axis0.requested_state = 1
            quit()

if __name__ == '__main__':
    main()