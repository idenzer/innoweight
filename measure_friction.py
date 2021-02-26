import odrive
import time

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
        odrv0.axis0.requested_state = 6 # Find index pulse
        time.sleep(3)

    try:
        print("Measuring friction")
        time.sleep(1)

        odrv0.axis0.motor.config.current_lim = 0.1
        odrv0.axis0.controller.config.control_mode = 3 # position control
        odrv0.axis0.requested_state = 8

        margin = 0.05 # 0.05 turns

        sum_current = 0
        iterations = 10

        for i in range(iterations):
            break_current = 0

            pos_start = odrv0.axis0.encoder.pos_estimate
            odrv0.axis0.controller.input_pos = pos_start + 0.25
            pos_curr = pos_start
            odrv0.axis0.motor.config.current_lim = 0.1

            while (pos_curr > pos_start - margin) and (pos_curr < pos_start + margin):
                odrv0.axis0.motor.config.current_lim += 0.05
                pos_curr = odrv0.axis0.encoder.pos_estimate
                print("start pos: ", pos_start, ". curr pos: ", pos_curr)
                print("current limit: ", odrv0.axis0.motor.config.current_lim)
                time.sleep(0.05)

            break_current = odrv0.axis0.motor.config.current_lim

            print("Breaking current ", i, " : ", break_current)
            sum_current += break_current
        average_break_current = sum_current / iterations

        print("\n Average break_current is: ", average_break_current)

    except:
        print("Exception raised")
    finally:
        odrv0.axis0.requested_state = 1
        print("Ending Program")
        quit()

if __name__ == '__main__':
    main()