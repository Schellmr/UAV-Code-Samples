import asyncio
import cv2
import math
import numpy as np
import os
import psutil
from cv2 import aruco
from mavsdk import System
from mavsdk.offboard import VelocityNedYaw
from statistics import mean
from time import time
from datetime import datetime

from overhead_landing import position_overhead

SER_ADDR = "serial:///dev/serial0:921600"
SIM_ADDR = "udp://:14540"

REFRESH_RATE = 1 / 30
VIDEO_REFRESH_RATE = 1/10
VIDEO_SAVE_RATE = 1  # save video every x number frames
FRAME_WIDTH = 640
FRAME_HEIGHT = 480
FOV_HORIZONTAL = 53.5
FOV_VERTICAL = FOV_HORIZONTAL * FRAME_HEIGHT / FRAME_WIDTH


class DroneSys(System):

    def __init__(self):
        super().__init__()
        self.roll_deg = 0
        self.pitch_deg = 0
        self.yaw_deg = 0

        self.alt_m = 9999
        self.stable_alt = False

        self.cX_down = 0
        self.cY_down = 0
        self.cX_dif = 0
        self.cY_dif = 0

        self.north_m = 0
        self.east_m = 0

        self.aruco10_detects = [0] * 20
        self.aruco45_detects = [0] * 20
        self.aruco_detected = False

        self.fps = 0

        self.north_set = 0
        self.east_set = 0

        self.update_video = True
        self.flying = True

    async def start_listeners(self):
        # start listeners & video
        await self.connect(system_address=SER_ADDR)

    async def print_ui(self):
        start_time = time()
        clear = lambda: os.system('clear')

        while True:
            if time() - start_time > .25:
                start_time = time()
                # clear()

                now = datetime.now()

                print(now.strftime("%m/%d/%y_%H:%M:%S"))
                print("CPU Utilization: %3.2f Memory Usage: %3.2f" % (psutil.cpu_percent(interval=None),
                                                                      psutil.virtual_memory().percent))
                print("Controller Input Rate: %4.2f" % self.fps)
                print("Roll: %5.2f Pitch: %5.2f Yaw: %6.2f" % (self.roll_deg, self.pitch_deg, self.yaw_deg))
                print("Altitude: %3.2f" % self.alt_m)
                print("Commanded Velocities: %3.2fN %3.2fE" % (self.north_set, self.east_set))
                print("FPS: %3.1f" % self.fps)
                print("Aruco Detected: " + str(self.aruco_detected))

                with open('log.txt', 'a') as f:
                    print(time(), file=f)
                    print("CPU Utilization: %3.2f Memory Usage: %3.2f" % (psutil.cpu_percent(interval=None),
                                                                          psutil.virtual_memory().percent), file=f)
                    print("Controller Input Rate: %4.2f" % self.fps, file=f)
                    print("Roll: %6.2f Pitch: %6.2f Yaw: %6.2f" % (self.roll_deg, self.pitch_deg, self.yaw_deg), file=f)
                    print("Altitude: %3.2f" % self.alt_m, file=f)
                    print("Commanded Velocities: %3.2fN %3.2fE" % (self.north_set, self.east_set), file=f)
                    print("FPS: %3.1f" % self.fps, file=f)
                    print("Aruco Detected: " + str(self.aruco_detected), file=f)

            await asyncio.sleep(.1)

    async def get_attitude(self):
        """
        This method gets attitude information including roll, pitch, and yaw.

        :return: void
        """

        print("Telem listener started.")
        async for telemetry in self.telemetry.attitude_euler():
            self.roll_deg = telemetry.roll_deg  # positive is banking right
            self.pitch_deg = telemetry.pitch_deg  # positive is nose up
            self.yaw_deg = telemetry.yaw_deg  # positive is clock-wise, from above

            self.cX_down = int(FRAME_WIDTH / 2 * (1 + self.roll_deg * 2 / FOV_HORIZONTAL))
            self.cY_down = int(FRAME_HEIGHT / 2 * (1 + self.pitch_deg * 2 / FOV_VERTICAL))

            if self.cX_down > FRAME_WIDTH - 1:
                self.cX_down = FRAME_WIDTH - 1
            if self.cX_down < 0:
                self.cX_down = 0
            if self.cY_down > FRAME_HEIGHT - 1:
                self.cY_down = FRAME_HEIGHT - 1
            if self.cY_down < 0:
                self.cY_down = 0

    async def get_altitude(self):
        """
        This method gets altitude information from the drone in centimeters and converts to meters.

        :return: void
        """

        # altitude returned from pixhawk is in CM, /100 to get m
        print("Altitude listener started.")
        altitudes = [0] * 10

        async for position in self.telemetry.distance_sensor():
            self.alt_m = position.current_distance_m / 100
            # relative altitude from takeoff point, in cm then converted to m

            altitudes.pop(9)
            altitudes.insert(0, self.alt_m)

            if max(altitudes) - min(altitudes) < 0.08:
                self.stable_alt = True
            else:
                self.stable_alt = False

    async def get_pi_video(self, save_video):
        """
        This method gets video from the pi in the format provided by the cv2 VideoCapture class.

        :param save_video: argument to allow for video saving or not
        :return: void
        """

        print("Pi video listener started.")
        video_src = cv2.VideoCapture(-1)  # open PiCam
        frame_width = int(video_src.get(3))
        frame_height = int(video_src.get(4))
        # find_aruco = ArucoFinder()

        if save_video:
            now = datetime.now()
            video_out = cv2.VideoWriter(now.strftime('%m%d%y_%H%M%S') + '.mp4',
                                        cv2.VideoWriter_fourcc('m', 'p', '4', 'v'), 1 / VIDEO_REFRESH_RATE / VIDEO_SAVE_RATE, (frame_width, frame_height))

        aruco_dict = aruco.custom_dictionary(0, 4, 1)
        aruco_dict.bytesList = np.empty(shape=(2, 2, 4), dtype=np.uint8)

        mybits = np.array([[1, 1, 1, 1], [1, 0, 0, 1], [1, 0, 0, 1], [0, 0, 0, 1]], dtype=np.uint8)  # ArUco 10
        aruco_dict.bytesList[0] = aruco.Dictionary_getByteListFromBits(mybits)
        mybits = np.array([[0, 0, 1, 0], [1, 1, 1, 0], [1, 1, 1, 0], [1, 0, 1, 1], ], dtype=np.uint8)  # ArUco 45
        aruco_dict.bytesList[1] = aruco.Dictionary_getByteListFromBits(mybits)

        parameters = aruco.DetectorParameters_create()
        parameters.errorCorrectionRate = 1
        dictionary = aruco_dict

        # dictionary = cv2.aruco.Dictionary_get(cv2.aruco.DICT_4X4_50)  # we should use a dict with only 45 and 10.
        # parameters = cv2.aruco.DetectorParameters_create()

        loop_time = time()
        frame_counter = 0

        while self.update_video:
            if time() - loop_time < VIDEO_REFRESH_RATE:
                await asyncio.sleep(VIDEO_REFRESH_RATE - (time() - loop_time))

            frame_counter += 1
            self.fps = 1 / (time() - loop_time)

            key = cv2.waitKey(1)
            if key == 27:  # esc key
                break

            loop_time = time()
            # await asyncio.sleep(REFRESH_RATE)

            self.aruco45_detects.pop(19)
            self.aruco10_detects.pop(19)

            _, frame = video_src.read()

            # (height, width) = frame.shape[:2]
            norm = np.zeros((frame_height, frame_width))
            norm_frame = cv2.normalize(frame, norm, 0, 255, cv2.NORM_MINMAX)

            gray = cv2.cvtColor(norm_frame, cv2.COLOR_BGR2GRAY)
            gaus_image = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 31, 4)

            marker_corners, marker_ids, _ = cv2.aruco.detectMarkers(image=gaus_image, dictionary=dictionary,
                                                                    parameters=parameters)
            if save_video & (frame_counter >= VIDEO_SAVE_RATE):
                frame_counter = 0
                aruco_frame = cv2.aruco.drawDetectedMarkers(frame, marker_corners, marker_ids)
                video_out.write(frame)

            if not marker_corners:  # no marker detected
                self.aruco10_detects.insert(0, 0)
                self.aruco45_detects.insert(0, 0)

                self.cX_dif = 0  # positive for move forward
                self.cY_dif = 0
                self.aruco_detected = False
            else:  # at least one marker detected
                self.aruco_detected = True
                for index in range(len(marker_ids)):  # iterate over detected arucos
                    if marker_ids[index] == 0:  # first check for 10, if 10 detected no need to look for 45.
                        c = marker_corners[index][0]
                        aruco10_xy = (c[:, 0].mean(), c[:, 1].mean())

                        self.aruco10_detects.insert(0, 1)
                        if mean(self.aruco10_detects) > mean(self.aruco45_detects):
                            self.cX_dif = aruco10_xy[0] - self.cX_down  # positive for move forward
                            self.cY_dif = self.cY_down - aruco10_xy[1]
                    else:  # 10 not detected, let's look for 45 now.
                        self.aruco10_detects.insert(0, 0)

                    if marker_ids[index] == 1:
                        c = marker_corners[index][0]
                        aruco45_xy = (c[:, 0].mean(), c[:, 1].mean())

                        self.aruco45_detects.insert(0, 1)
                        if mean(self.aruco45_detects) > mean(self.aruco10_detects):
                            self.cX_dif = aruco45_xy[0] - self.cX_down  # positive for move forward
                            self.cY_dif = self.cY_down - aruco45_xy[1]
                    else:
                        self.aruco45_detects.insert(0, 0)

                north_pix = self.cY_dif * math.cos(math.radians(self.yaw_deg)) - self.cX_dif * \
                            math.sin(math.radians(self.yaw_deg))
                east_pix = self.cX_dif * math.cos(math.radians(self.yaw_deg)) + self.cY_dif * \
                           math.sin(math.radians(self.yaw_deg))

                # distance error = cos(FOV/2) * pixels / (MAX_PIXELS / 2) * alt_m
                self.north_m = north_pix * 0.00279 * self.alt_m  # updated for PiCam 480p
                self.east_m = east_pix * 0.00279 * self.alt_m

        video_src.release()  # **************** I THINK WE HAVE TO CALL THIS WHEN WE EXIT *****************

        if save_video:
            pass
            # video_out.release()  # maybe not tho

    async def set_velocities(self, landing, adaptive):
        """
        This method will constantly update the drone with new velocities. It places the drone into offboard mode.

        :param landing: determines whether to descend
        :param adaptive: use adaptive landing velocities
        :return: void
        """
        await self.offboard.set_velocity_ned(VelocityNedYaw(0.0, 0.0, 0.0, 0.0))
        await self.offboard.start()
        print("Offboard started.")

        north_prev = 0
        east_prev = 0

        start_time = time()
        await asyncio.sleep(2)

        while True:
            await asyncio.sleep(REFRESH_RATE)
            if self.flying & (mean(self.aruco45_detects) > 0.1 or mean(self.aruco10_detects) > 0.1):
                break

        while self.flying & (mean(self.aruco45_detects) > 0.1 or mean(self.aruco10_detects) > 0.1):  # arbitrary %
            self.north_set, self.east_set, _ = position_overhead(self.north_m, self.east_m, north_prev, east_prev, 0, 0)

            if adaptive and self.north_m < north_prev and self.east_m < east_prev:
                alt_set = self.alt_m * .1 if self.alt_m > 1 else .125
            else:
                alt_set = 0.125 if landing else 0

            await self.offboard.set_velocity_ned(
                VelocityNedYaw(self.north_set, self.east_set, alt_set, 0.0))  # positive z is down
            north_prev = self.north_set
            east_prev = self.east_set

            await asyncio.sleep(REFRESH_RATE)

            if time() - start_time > 2:
                print(self.north_set, self.east_set)
                start_time = time()

            if self.stable_alt and self.alt_m < 0.12:
                self.flying = False

        await self.offboard.stop()
        print("Stopping offboard.")

        if not self.flying:
            await self.action.kill()
            print("Landed or crashed, I dunno.")
