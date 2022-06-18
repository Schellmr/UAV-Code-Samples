import time

from mavlink.mavlink_class import MavRcvr
from util.video_capture import Video
from util.adaptive_center import Center
from util.aruco_center import FindAruco
from util.overhead_landing import position_overhead
from cv2 import cv2
import numpy as np

if __name__ == '__main__':
    # Create the video object
    video = Video()
    # rcvr = MavRcvr()
    find_aruco = FindAruco()
    center = Center(320, 240)
    font = cv2.FONT_HERSHEY_COMPLEX

    old_north = 0
    old_east = 0
    prev_altitude = 0

    Drone = MavRcvr()
    Drone.set_offboard_mode()
    Drone.set_velocity(0,0,0,0)

    while True:
        time.sleep(.01)
        key = cv2.waitKey(1)
        if key == 27:  # esc key
            break
        # Wait for the next frame
        if not video.frame_available():
            continue

        if Drone.get_attitude() != 0:
            continue

        if Drone.get_altitude() != 0:
            continue

        frame = video.frame()
        (height, width) = frame.shape[:2]
        norm = np.zeros((height, width))
        norm_frame = cv2.normalize(frame, norm, 0, 255, cv2.NORM_MINMAX)

        cX, cY = center.find_center(Drone.roll, Drone.pitch)
        # cv2.circle(norm_frame, (cX, cY), 3, (255, 255, 255), -1)

        if not find_aruco.is_aruco(norm_frame):
            cv2.imshow('Quad Video', norm_frame)
            continue

        cX_aruco, cY_aruco = find_aruco.return_center()
        cv2.circle(norm_frame, (cX_aruco, cY_aruco), 3, (255, 255, 255), -1)

        desired_north = cY - cY_aruco
        desired_east = cX - cX_aruco

        north_velo, east_velo, alt_velo = position_overhead(desired_north, -desired_east, old_north, old_east,
                                                            Drone.altitude / 1000, prev_altitude / 1000)

        prev_altitude = Drone.altitude
        old_north = desired_north
        old_east = -desired_east

        # print(north_velo)
        # print(east_velo)

        #Drone.set_velocity(north_velo, east_velo, alt_velo, 0)

        time.sleep(0.01)
        # cv2.putText(norm_frame, str(rcvr.roll), (50, 50), font, 1, (0, 0, 255))
        # cv2.putText(norm_frame, str(rcvr.pitch), (50, 100), font, 1, (0, 0, 255))

        cv2.imshow('Quad Video', norm_frame)

cv2.destroyAllWindows()
