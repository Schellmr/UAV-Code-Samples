from pymavlink import mavutil
from time import time_ns


class MavCtrl:
    roll = 0
    pitch = 0
    time_att = time_ns()
    altitude = 0 # in mm

    def __init__(self):
        self.connection = mavutil.mavlink_connection('udpin:localhost:14540')
        self.connection.wait_heartbeat()
        print("Mavlink connected.")

    def get_attitude(self):
        msg = self.connection.recv_match(type='ATTITUDE', blocking=True, timeout=1e-3)

        if msg:
            self.roll = msg.roll
            self.pitch = msg.pitch
            self.time_att = time_ns()
            return 0

        elif time_ns() - self.time_att > 1e9:
            self.roll = 0
            self.pitch = 0

        return 1

    def get_altitude(self):
        msg = self.connection.recv_match(type='GLOBAL_POSITION_INT', blocking=True, timeout=1e-3)

        if msg:
            self.altitude = msg.relative_alt
            return 0

        return 1

    # def send_off_vel(self):
        # self.connection.mav.