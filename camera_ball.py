import cv2
import numpy as np
from PID import calculateAngle
from time import sleep

camera = cv2.VideoCapture(2)

if not (camera.isOpened()):
    print("Could not open video device")
    exit()

def visualize(xy, img):
    img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)

    img = cv2.circle(img, xy, 5, (0, 0, 255))

    m1_pos, m1_far = (225, 55), (400, 390)
    m2_pos, m2_far = (210, 390), (400, 50)
    m3_pos, m3_far = (490, 240), (100, 230)

    # ang = calculateAngle((m1_pos, m1_far), (m1_pos, xy))
    # print(ang)

    img = cv2.line(img, m1_pos, m1_far, (0, 255, 0))
    img = cv2.line(img, m2_pos, m2_far, (0, 255, 0))
    img = cv2.line(img, m3_pos, m3_far, (0, 255, 0))

    img = cv2.putText(img, "m1", m1_pos, cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
    img = cv2.putText(img, "m2", m2_pos, cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
    img = cv2.putText(img, "m3", m3_pos, cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

    img = cv2.putText(img, "m1_far", m1_far, cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
    img = cv2.putText(img, "m2_far", m2_far, cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
    img = cv2.putText(img, "m3_far", m3_far, cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

    cv2.imshow("test", img)
    cv2.waitKey(0)


def get_ball_loc():
    global camera
    ret, img = camera.read()

    img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    lower = np.array([60, 45, 0], dtype="uint8")
    upper = np.array([90, 255, 255], dtype="uint8")
    img = cv2.inRange(img, lower, upper)

    cnts, _ = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    big = None

    big_int = 0
    for c in cnts:
        if c.shape[0] > big_int and c.shape[0] > 50:
            big_int = 0
            big = c

    if big is None:
        return None, None

    x, y = 0, 0
    for i in big:
        x += i[0][0]
        y += i[0][1]

    x = int(x / len(big))
    y = int(y / len(big))

    return (x, y), img