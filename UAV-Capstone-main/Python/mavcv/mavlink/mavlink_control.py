import threading

from pymavlink import mavutil
from time import time_ns
from time import time
from time import sleep


class MavCtrl:
    run = True

    roll = 0
    pitch = 0
    att_time = time_ns()
    att_good = False

    altitude = 0  # in mm
    alt_time = time_ns()
    alt_good = False

    vx_set = 0
    vy_set = 0
    vz_set = 0
    yaw_set = 0

    state = 0  # state variable for changing modes
    # 2 equals offboard velo command

    def __init__(self):
        self.connection = mavutil.mavlink_connection('udpin:localhost:14540')
        self.connection.wait_heartbeat()
        print("Mavlink connected.")
        msg = self.connection.recv_match(type=['LOCAL_POSITION_NED'], blocking=True)
        self.time_offset_ms = msg.time_boot_ms - int(round(time() * 1000))
        print("Time initialized.")
        self.listen_thread = threading.Thread(target=self.combined)
        self.offboard_thread = threading.Thread(target=self.set_offboard())

    def listen(self):
        msg = self.connection.recv_match(blocking=True, timeout=1e-3)
        if not msg:
            return

        msg_type = msg.get_type()
        if msg_type == "ATTITUDE":
            self.roll = msg.roll
            self.pitch = msg.pitch
            self.att_time = time_ns()
            self.att_good = True
            return 0

        elif msg_type == "GLOBAL_POSITION_INT":
            self.altitude = msg.relative_alt
            self.alt_time = time_ns()
            self.alt_good = True
            return 0

    def check_data(self):
        if time_ns() - self.att_time > 1e9:
            self.roll = 0
            self.pitch = 0
            self.att_good = False

        if time_ns() - self.alt_time > 1e9:
            self.alt_good = False

        return 0

    def combined(self):
        while True:
            self.listen()
            self.check_data()

    def start_listener(self):
        self.listen_thread.start()
        print("Listener started.")

    def init_offboard(self):
        self.connection.mav.command_long_send(1, 1, mavutil.mavlink.MAV_CMD_DO_SET_MODE, 0, 1, 6, 0, 0, 0, 0, 0)

    def set_velocity(self):  # (self, vx, vy, vz, yaw):
        time_boot_ms = int(time() * 1000) + self.time_offset_ms
        type_mask = 0b0000101111000111  # ignore everything but x, y, z velocities and set yaw

        self.connection.mav.set_position_target_local_ned_send(time_boot_ms, 1, 1, mavutil.mavlink.MAV_FRAME_LOCAL_NED,
                                                               type_mask, 0, 0, 0, self.vx_set, self.vy_set,
                                                               self.vz_set, 0, 0, 0, self.yaw_set, 0)
        return 0

    def set_offboard(self):
        self.init_offboard()
        while self.state == 2:
            self.set_velocity()
            sleep(0.1)

    def start_offboard(self):
        self.offboard_thread.start()
        print("Offboard started @10Hz.")
