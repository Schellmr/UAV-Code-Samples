from mavsdk import System


class DroneSys(System):

    def __init__(self):
        super().__init__()
        self.roll_deg = 0
        self.pitch_deg = 0
        self.yaw_deg = 0

        self.alt_m = 0
        self.stable_alt = False

        self.cX_down = 0
        self.cY_down = 0
        self.cX_dif = 0
        self.cY_dif = 0

        self.aruco10_detects = [0] * 20
        self.aruco45_detects = [0] * 20

        self.update_video = True
        self.flying = True
