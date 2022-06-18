from video_capture import Video
from adaptive_center import Center
from aruco_center import FindAruco
from overhead_landing import position_overhead
from cv2 import cv2
import numpy as np


class CVStuff:
    # Create the video object
    video = Video()
    # rcvr = MavRcvr()
    find_aruco = FindAruco()
    center = Center(320, 240)
    font = cv2.FONT_HERSHEY_COMPLEX

    old_north = 0
    old_east = 0
    old_alt = 0

    def find_velos(self, pitch, roll, alt):

        if not self.video.frame_available():
            return 0, 0, 0, 0

        frame = self.video.frame()
        (height, width) = frame.shape[:2]
        norm = np.zeros((height, width))
        norm_frame = cv2.normalize(frame, norm, 0, 255, cv2.NORM_MINMAX)

        cX, cY = self.center.find_center(roll, pitch)
        cv2.circle(norm_frame, (cX, cY), 3, (255, 255, 255), -1)

        if not self.find_aruco.is_aruco(norm_frame):
            cv2.imshow('Quad Video', norm_frame)
            return 0, 0, 0, 0

        cX_aruco, cY_aruco = self.find_aruco.return_center()
        cv2.circle(norm_frame, (cX_aruco, cY_aruco), 3, (255, 255, 255), -1)

        desired_north = cY - cY_aruco
        desired_east = cX_aruco - cX

        north_velo, east_velo, _ = position_overhead(desired_north, desired_east, self.old_north, self.old_east, 0, 0)

        self.old_north = desired_north
        self.old_east = desired_east

        # print(north_velo)
        # print(east_velo)

        cv2.imshow('Quad Video', norm_frame)

        return north_velo, east_velo, 0, 0
        # Drone.set_velocity(north_velo, east_velo, 0, 0)

        # time.sleep(0.01)
        # cv2.putText(norm_frame, str(rcvr.roll), (50, 50), font, 1, (0, 0, 255))
        # cv2.putText(norm_frame, str(rcvr.pitch), (50, 100), font, 1, (0, 0, 255))

    # def close(self):
    #     cv2.destroyAllWindows()

