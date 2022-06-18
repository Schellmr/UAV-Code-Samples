from pymavlink import mavutil
from time import time_ns
import time


class MavRcvr:
    roll = 0
    pitch = 0
    time_att = time_ns()
    altitude = 0  # in mm

    def __init__(self):
        self.connection = mavutil.mavlink_connection('udpin:localhost:14540')
        self.connection.wait_heartbeat()
        print("Mavlink connected.")
        msg = self.connection.recv_match(type=['LOCAL_POSITION_NED'], blocking=True)
        # print('LOCAL_POSITION_NED: ', msg.time_boot_ms)
        # px4_time_boot_msec = msg.time_boot_ms
        # initial_msec = int(round(time.time() * 1000))
        self.time_offset_ms = msg.time_boot_ms - int(round(time.time() * 1000))
        print("Time initialized.")

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

    def set_position_ned(self, difference_north, difference_east, difference_altitude):


        return 0

    def set_velocity(self, vx, vy, vz, yaw):
        time_boot_msec = int(time.time() * 1000) + self.time_offset_ms
        type_mask = 0b0000101111000111  # ignore everything by x, y, z velocities and set yaw
        # mav.mav.set_position_target_local_ned_send(time_boot_ms, 1, 1, mavutil.mavlink.MAV_FRAME_BODY_FRD,
        # type_mask, 0, 0, 0, vx, vy, vz, 0, 0, 0, yaw, 0)
        self.connection.mav.set_position_target_local_ned_send(time_boot_msec, 1, 1,
                                                               mavutil.mavlink.MAV_FRAME_LOCAL_NED, type_mask, 0, 0, 0,
                                                               vx, vy, vz, 0, 0, 0, yaw, 0)
        return 0

    def set_offboard_mode(self):
        self.connection.mav.command_long_send(1, 1, mavutil.mavlink.MAV_CMD_DO_SET_MODE, 0, 1, 6, 0, 0, 0, 0, 0)
        # offboard mode = 216, disarm might = 88
        # preflight = 0
