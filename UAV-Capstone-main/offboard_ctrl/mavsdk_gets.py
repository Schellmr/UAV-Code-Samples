import asyncio
import cv2
import numpy as np
import math

from aruco_center import ArucoFinder
from video_capture import Video
from mavsdk.offboard import VelocityNedYaw
from overhead_landing import position_overhead
from time import time_ns
from time import time
from statistics import mean

REFRESH_RATE = 1 / 30
FRAME_WIDTH = 320
FRAME_HEIGHT = 240
FOV_HORIZONTAL = 62.2
FOV_VERTICAL = FOV_HORIZONTAL * FRAME_HEIGHT / FRAME_WIDTH


async def get_telemetry(drone):
    times = [0] * 10
    time_prev = time_ns()

    async for telemetry in drone.telemetry.attitude_euler():
        time_itt = time_ns()
        times.insert(0, time_itt - time_prev)
        times.pop(10)
        time_prev = time_itt
        # print("Telemetry refresh rate, in Hz: ", 1 / mean(times) * 1e9)

        drone.roll_deg = telemetry.roll_deg  # positive is banking right
        drone.pitch_deg = telemetry.pitch_deg  # positive is nose up
        drone.yaw_deg = telemetry.yaw_deg  # positive is clock-wise, from above

        # get_center(drone, 320, 240, 62.2)
        # h_fov = 62.2
        # height = 240
        # width = 320
        # v_fov = h_fov * height / width  # find vertical
        # print("Adaptive center refresh rate, in Hz: ", 1 / mean(times) * 1e9)

        drone.cX_down = int(FRAME_WIDTH / 2 * (1 + drone.roll_deg * 2 / FOV_HORIZONTAL))
        drone.cY_down = int(FRAME_HEIGHT / 2 * (1 + drone.pitch_deg * 2 / FOV_VERTICAL))

        if drone.cX_down > FRAME_WIDTH - 1:
            drone.cX_down = FRAME_WIDTH - 1

        if drone.cX_down < 0:
            drone.cX_down = 0

        if drone.cY_down > FRAME_HEIGHT - 1:
            drone.cY_down = FRAME_HEIGHT - 1

        if drone.cY_down < 0:
            drone.cY_down = 0

        # print(drone.cX_down, drone.cY_down)
        # print("here")

        # print(drone.roll_deg)
        # print(drone.pitch_deg)
        # print(drone.yaw_deg)


async def get_altitude(drone):
    times = [0] * 10
    time_prev = time_ns()

    altitudes = [0] * 30

    async for position in drone.telemetry.position():
        time_itt = time_ns()
        times.insert(0, time_itt - time_prev)
        times.pop(10)
        time_prev = time_itt
        # print("Altitude refresh rate, in Hz: ", 1/mean(times)*1e9)

        drone.alt_m = position.relative_altitude_m  # relative altitude from takeoff point, in meters

        altitudes.pop(29)
        altitudes.insert(0, position.relative_altitude_m)

        if max(altitudes) - min(altitudes) < 0.03:
            drone.stable_alt = True
        else:
            drone.stable_alt = False
        # print(drone.alt_m)


async def get_video(drone):
    video_src = Video()
    # find_aruco = ArucoFinder()
    times = [0] * 10
    time_prev = time_ns()

    dictionary = cv2.aruco.Dictionary_get(cv2.aruco.DICT_4X4_50)
    parameters = cv2.aruco.DetectorParameters_create()

    while drone.update_video:
        await asyncio.sleep(REFRESH_RATE)

        key = cv2.waitKey(1)
        if key == 27:  # esc key
            break
        # Wait for the next frame
        if not video_src.frame_available():
            continue

        time_itt = time_ns()
        times.insert(0, time_itt - time_prev)
        times.pop(10)
        time_prev = time_itt
        # print("Video refresh rate, in Hz: ", 1 / mean(times) * 1e9)

        drone.aruco45_detects.pop(19)
        drone.aruco10_detects.pop(19)

        frame = video_src.frame()

        # (height, width) = frame.shape[:2]
        norm = np.zeros((FRAME_HEIGHT, FRAME_WIDTH))
        norm_frame = cv2.normalize(frame, norm, 0, 255, cv2.NORM_MINMAX)

        marker_corners, marker_ids, _ = cv2.aruco.detectMarkers(image=norm_frame, dictionary=dictionary,
                                                                parameters=parameters)

        if not marker_corners:
            drone.aruco10_detects.insert(0, 0)
            drone.aruco45_detects.insert(0, 0)

            drone.cX_dif = 0  # positive for move forward
            drone.cY_dif = 0

        else:
            aruco10_xy = False
            aruco45_xy = False

            for i in range(len(marker_ids)):
                if marker_ids[i] == 45:
                    c = marker_corners[i][0]
                    aruco45_xy = (c[:, 0].mean(), c[:, 1].mean())

                elif marker_ids[i] == 10:
                    c = marker_corners[i][0]
                    aruco10_xy = (c[:, 0].mean(), c[:, 1].mean())

            if aruco45_xy:
                drone.aruco45_detects.insert(0, 1)
                cv2.circle(norm_frame, aruco45_xy, 7, (255, 255, 255), -1)
                if mean(drone.aruco45_detects) > mean(drone.aruco10_detects):
                    drone.cX_dif = aruco45_xy[0] - drone.cX_down  # positive for move forward
                    drone.cY_dif = drone.cY_down - aruco45_xy[1]
            else:
                drone.aruco45_detects.insert(0, 0)

            if aruco10_xy:
                drone.aruco10_detects.insert(0, 1)
                cv2.circle(norm_frame, aruco10_xy, 3, (1, 1, 255), -1)
                if mean(drone.aruco10_detects) > mean(drone.aruco45_detects):
                    drone.cX_dif = aruco10_xy[0] - drone.cX_down  # positive for move forward
                    drone.cY_dif = drone.cY_down - aruco10_xy[1]
            else:
                drone.aruco10_detects.insert(0, 0)

            # drone.cX_dif = drone.cX_aruco - drone.cX  # positive for move forward
            # drone.cY_dif = drone.cY - drone.cY_aruco

        cv2.putText(norm_frame, "Video FPS: " + str(int(1 / mean(times) * 1e9)), (10, 16), cv2.FONT_HERSHEY_COMPLEX,
                    0.4, (255, 255, 255))

        cv2.circle(norm_frame, (drone.cX_down, drone.cY_down), 3, (255, 255, 255), -1)
        cv2.imshow('Quad Video', norm_frame)

    cv2.destroyAllWindows()


async def get_pivideo(drone):
    print("Video listener actually started.")
    video_src = cv2.VideoCapture(-1)
    # find_aruco = ArucoFinder()
    times = [0] * 10
    time_prev = time_ns()

    dictionary = cv2.aruco.Dictionary_get(cv2.aruco.DICT_4X4_50)
    parameters = cv2.aruco.DetectorParameters_create()

    start_time = time()

    while drone.update_video:
        await asyncio.sleep(REFRESH_RATE)

        key = cv2.waitKey(1)
        if key == 27:  # esc key
            break
        # Wait for the next frame

        time_itt = time_ns()
        times.insert(0, time_itt - time_prev)
        times.pop(10)
        time_prev = time_itt
        # print("Video refresh rate, in Hz: ", 1 / mean(times) * 1e9)

        drone.aruco45_detects.pop(19)
        drone.aruco10_detects.pop(19)

        _, frame = video_src.read()

        # (height, width) = frame.shape[:2]
        norm = np.zeros((FRAME_HEIGHT, FRAME_WIDTH))
        norm_frame = cv2.normalize(frame, norm, 0, 255, cv2.NORM_MINMAX)

        marker_corners, marker_ids, _ = cv2.aruco.detectMarkers(image=norm_frame, dictionary=dictionary,
                                                                parameters=parameters)

        if not marker_corners:
            drone.aruco10_detects.insert(0, 0)
            drone.aruco45_detects.insert(0, 0)

            drone.cX_dif = 0  # positive for move forward
            drone.cY_dif = 0

        else:
            aruco10_xy = False
            aruco45_xy = False

            for i in range(len(marker_ids)):
                if marker_ids[i] == 45:
                    c = marker_corners[i][0]
                    aruco45_xy = (c[:, 0].mean(), c[:, 1].mean())

                elif marker_ids[i] == 10:
                    c = marker_corners[i][0]
                    aruco10_xy = (c[:, 0].mean(), c[:, 1].mean())

            if aruco45_xy:
                drone.aruco45_detects.insert(0, 1)
                # cv2.circle(norm_frame, aruco45_xy, 7, (255, 255, 255), -1)
                if mean(drone.aruco45_detects) > mean(drone.aruco10_detects):
                    drone.cX_dif = aruco45_xy[0] - drone.cX_down  # positive for move forward
                    drone.cY_dif = drone.cY_down - aruco45_xy[1]
            else:
                drone.aruco45_detects.insert(0, 0)

            if aruco10_xy:
                drone.aruco10_detects.insert(0, 1)
                # cv2.circle(norm_frame, aruco10_xy, 3, (1, 1, 255), -1)
                if mean(drone.aruco10_detects) > mean(drone.aruco45_detects):
                    drone.cX_dif = aruco10_xy[0] - drone.cX_down  # positive for move forward
                    drone.cY_dif = drone.cY_down - aruco10_xy[1]
            else:
                drone.aruco10_detects.insert(0, 0)

            # drone.cX_dif = drone.cX_aruco - drone.cX  # positive for move forward
            # drone.cY_dif = drone.cY - drone.cY_aruco

        # cv2.putText(norm_frame, "Video FPS: " + str(int(1 / mean(times) * 1e9)), (10, 16), cv2.FONT_HERSHEY_COMPLEX,
        #             0.4, (255, 255, 255))

        # cv2.circle(norm_frame, (drone.cX_down, drone.cY_down), 3, (255, 255, 255), -1)
        # cv2.imshow('Quad Video', norm_frame)

        if time() - start_time > 3:
            print("X pixels difference: ", drone.cX_dif, "and Y pixels difference: ", drone.cY_dif)
            start_time = time()
    # cv2.destroyAllWindows()


async def set_descent(drone):
    await drone.offboard.set_velocity_ned(VelocityNedYaw(0.0, 0.0, 0.0, 0.0))
    await drone.offboard.start()
    print("Offboard started.")

    north_prev = 0
    east_prev = 0

    # print("Waiting for 3 second.")
    # await asyncio.sleep(3)

    while drone.flying:  # while mean(drone.aruco_detects) > 0.25:  # arbitrary %

        north_pix = drone.cY_dif * math.cos(math.radians(drone.yaw_deg)) - drone.cX_dif * \
                    math.sin(math.radians(drone.yaw_deg))

        east_pix = drone.cX_dif * math.cos(math.radians(drone.yaw_deg)) + drone.cY_dif * \
                    math.sin(math.radians(drone.yaw_deg))

        north_m = north_pix * 0.00377 * drone.alt_m
        east_m = east_pix * 0.00377 * drone.alt_m
        north_set, east_set, _ = position_overhead(north_m, east_m, north_prev, east_prev, 0, 0)

        await drone.offboard.set_velocity_ned(VelocityNedYaw(north_set, east_set, 0.25, 0.0))
        north_prev = north_set
        east_prev = east_set

        await asyncio.sleep(REFRESH_RATE)

        if (mean(drone.aruco10_detects) > 0.9) & drone.stable_alt:
            drone.flying = False

    await drone.offboard.stop()
    await drone.action.kill()
    # print("Landing.")
    # await drone.action.land()
