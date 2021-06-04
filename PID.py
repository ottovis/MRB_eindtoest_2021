import math


def calculateNearSide(angle, len_long_side):
    return math.cos(angle) * len_long_side


def calculateDistance(xy1, xy2):
    dist = math.sqrt((xy1[0] - xy2[0]) ** 2 + (xy1[1] - xy2[1]) ** 2)
    return dist


def gradiant(p1, p2):
    try:
        val = (p1[1] - p2[1]) / (p1[0] - p2[0])
    except ZeroDivisionError:
        print("Zero 1 p1:", p1, "p2:", p2)
        return (p1[1] - p2[1])
    return val


def calculateAngle(line1, line2):
    p1, p2 = line1
    _, p3 = line2
    m1 = gradiant(p1, p2)
    m2 = gradiant(p1, p3)
    try:
        val = abs(math.atan((m2 - m1) / (1 + m2 * m1)))
    except ZeroDivisionError:
        print("Zero 2 m1:", m1, "m2:", m2)
        return (m2 - m1)
    return val


class PID_regelaar:
    def __init__(self):
        self.global_bias = 110

        self.p_bias = 0
        self.p_weight = 1/20
        self.p_last = None

        self.i_bias = 0
        self.i_weight = 1/1000
        self.i_memory = [0]
        self.i_last = None

        self.d_bias = 0
        self.d_weight = 1.1
        self.d_memory = None
        self.d_last = None

    def p_regel(self, err):
        command = int(self.p_bias + self.p_weight * err)

        if self.p_last is None:
            self.p_last = command

        if command == self.p_last - 1 or command == self.p_last + 1:
            return self.p_last

        self.p_last = command
        return command


    def i_regel(self, err):
        if len(self.i_memory) > 50:
            self.i_memory.pop(0)

        self.i_memory.append(err)
        # print(sum(self.i_memory))
        command = int(self.i_bias + sum(self.i_memory) * self.i_weight)

        if self.i_last is None:
            self.i_last = command

        if command == self.i_last - 1 or command == self.i_last + 1:
            return self.i_last

        self.i_last = command
        return command


    def d_regel(self, err):
        if self.d_memory is None:
            self.d_memory = err
            return self.d_bias

        actie = self.d_memory - err
        self.d_memory = err

        command = 0 - (self.d_bias + self.d_weight * actie)

        if self.d_last is None:
            self.d_last = command

        if command == self.d_last - 1 or command == self.d_last + 1:
            return self.d_last

        self.d_last = command
        return command

    def regel(self, err):
        command = self.global_bias
        command += self.p_regel(err)
        command += self.i_regel(err)
        command += self.d_regel(err)

        return int(command)


def get_error(xy_ball, xy_sp):
    m1_pos, m1_far = (225, 55), (400, 390)
    m2_pos, m2_far = (210, 390), (400, 50)
    m3_pos, m3_far = (490, 240), (100, 230)

    # m1_angle_ball = calculateAngle((m1_pos, m1_far), (m1_pos, xy_ball))
    # m1_abs_dist_ball = calculateDistance(m1_pos, xy_ball)
    # m1_dis_to_ball = calculateNearSide(m1_angle_ball, m1_abs_dist_ball)
    #
    # print("\nangle:", m1_angle_ball)
    # print("abs_dist:", m1_abs_dist_ball)
    # print("m1_effective:", m1_dis_to_ball, "\n")

    m1_dis_to_ball = calculateNearSide(calculateAngle((m1_pos, m1_far), (m1_pos, xy_ball)),
                                       calculateDistance(m1_pos, xy_ball))
    m2_dis_to_ball = calculateNearSide(calculateAngle((m2_pos, m2_far), (m2_pos, xy_ball)),
                                       calculateDistance(m2_pos, xy_ball))
    m3_dis_to_ball = calculateNearSide(calculateAngle((m3_pos, m3_far), (m3_pos, xy_ball)),
                                       calculateDistance(m3_pos, xy_ball))

    m1_dis_to_sp = calculateNearSide(calculateAngle((m1_pos, m1_far), (m1_pos, xy_sp)),
                                     calculateDistance(m1_pos, xy_sp))
    m2_dis_to_sp = calculateNearSide(calculateAngle((m2_pos, m2_far), (m2_pos, xy_sp)),
                                     calculateDistance(m2_pos, xy_sp))
    m3_dis_to_sp = calculateNearSide(calculateAngle((m3_pos, m3_far), (m3_pos, xy_sp)),
                                     calculateDistance(m3_pos, xy_sp))
    return m1_dis_to_ball - m1_dis_to_sp, m2_dis_to_ball - m2_dis_to_sp, m3_dis_to_ball - m3_dis_to_sp
