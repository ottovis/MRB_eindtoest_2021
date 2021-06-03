from serial_due import *
from camera_ball import *
from PID import *

from time import sleep

xy_sp = (310, 240)

def get_setpoint():
    with open("setpoint.txt", "r") as file:
        read = file.read()
        read = read.split(',')
        x, y = int(read[0]), int(read[1])
    return x, y

if __name__ == '__main__':
    # input("Reset due before continuing. Press Enter when ready")
    if not check_connected():
        assert False, "Must be connected to the due"

    m0 = PID_regelaar()
    m1 = PID_regelaar()
    m2 = PID_regelaar()

    while True:
        xy_sp = get_setpoint()
        xy_ball, img = get_ball_loc()
        if xy_ball is None:
            continue

        # visualize(xy_ball, img)
        # print("xy_ball", xy_ball)

        xyz_error = get_error(xy_ball, xy_sp)
        # print("xyz_error", xyz_error)

        rs0, rs1, rs2 = m0.regel(xyz_error[0]), m1.regel(xyz_error[1]), m2.regel(xyz_error[2])
        # print("rs", rs0, rs1, rs2)

        send_motor_coordinates(rs0, rs1, rs2)














