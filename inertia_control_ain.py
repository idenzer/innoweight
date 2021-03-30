import odrive
import time

Kt = 8.27/150
deadband = 0.5 # [turns]
target_torque = 0.2
min_torque = 0

acc_coeff = 0.005#0.01848226678

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

    odrv0.axis0.motor.config.current_lim = 10
    odrv0.axis0.controller.config.control_mode = 1 # torque control
    odrv0.axis0.requested_state = 8 # closed loop control
    pos_init = odrv0.axis0.encoder.pos_estimate
    slope_torque = min_torque + (target_torque - min_torque) / deadband

    prev_vel = odrv0.axis0.encoder.vel_estimate
    curr_vel = odrv0.axis0.encoder.vel_estimate

    prev_t = time.time()
    curr_t = time.time()

    while True:
        try:
            pos_curr = odrv0.axis0.encoder.pos_estimate
            pos_error = pos_curr - pos_init

            prev_vel = curr_vel
            curr_vel = odrv0.axis0.encoder.vel_estimate

            prev_t = curr_t
            curr_t = time.time()

            acc = (curr_vel - prev_vel) / (curr_t - prev_t)

            if pos_error < 0:
                odrv0.axis0.controller.input_torque = -min_torque
            elif pos_error < deadband:
                odrv0.axis0.controller.input_torque = -pos_error * slope_torque
            else:
                print("acc: ", (acc_coeff * acc))
                odrv0.axis0.controller.input_torque = -target_torque - (acc_coeff * acc)

            #print("Current torque: ", odrv0.axis0.controller.input_torque)
        except Exception as e:
            odrv0.axis0.requested_state = 1
            print(str(e))
            print("Exited program. Dumping errors.")
            quit()

if __name__ == '__main__':
    main()