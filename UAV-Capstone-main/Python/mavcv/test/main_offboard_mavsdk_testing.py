import asyncio

import numpy as np
from mavsdk import System
from mavsdk.offboard import (OffboardError, VelocityNedYaw)
from util.video_capture import Video
from util.adaptive_center import Center
from util.aruco_center import FindAruco
from util.overhead_landing import position_overhead
from cv2 import cv2


async def get_altitude(drone):
    """ Prints the altitude when it changes """

    previous_altitude = None

    async for position in drone.telemetry.position():
        altitude = round(position.relative_altitude_m)
        if altitude != previous_altitude:
            previous_altitude = altitude
            return altitude


async def get_attitude(drone):
    """ Prints the attitude when it changes """

    previous_attitude = None

    async for attitude in drone.telemetry.attitude_euler():
        if attitude != previous_attitude:
            previous_attitude = attitude
            return [attitude.roll_deg, attitude.pitch_deg]


async def run():
    """ Does Offboard control using velocity NED coordinates. """

    drone = System()
    await drone.connect(system_address="udp://:14540")

    print("Waiting for drone to connect...")
    async for state in drone.core.connection_state():
        if state.is_connected:
            print(f"Drone discovered!")
            break

    print("-- Arming")
    await drone.action.arm()

    print("-- Setting initial setpoint")
    await drone.offboard.set_velocity_ned(VelocityNedYaw(0.0, 0.0, 0.0, 0.0))

    print("-- Starting offboard")
    try:
        await drone.offboard.start()
    except OffboardError as error:
        print(f"Starting offboard mode failed with error code: \
                  {error._result.result}")
        print("-- Disarming")
        await drone.action.disarm()
        return

    # Create the video object
    video = Video()
    # rcvr = MavRcvr()
    find_aruco = FindAruco()
    center = Center(320, 240)
    font = cv2.FONT_HERSHEY_COMPLEX
    old_north = 0
    old_east = 0
    prev_altitude = 0

    while True:
        key = cv2.waitKey(1)
        if key == 27:  # esc key
            break
        # Wait for the next frame
        if not video.frame_available():
            continue

        frame = video.frame()
        (height, width) = frame.shape[:2]
        norm = np.zeros((height, width))
        norm_frame = cv2.normalize(frame, norm, 0, 255, cv2.NORM_MINMAX)

        attitude = await get_attitude(drone)
        altitude = await get_altitude(drone)

        center_x, center_y = center.find_center(attitude[0], attitude[1])

        if not find_aruco.is_aruco(norm_frame):
            cv2.imshow('Quad Video', norm_frame)
            continue

        center_x_aruco, center_y_aruco = find_aruco.return_center()
        cv2.circle(norm_frame, (center_x_aruco, center_y_aruco), 3, (255, 255, 255), -1)

        desired_north = center_y - center_y_aruco
        desired_east = center_x - center_x_aruco

        north_velo, east_velo, alt_velo = position_overhead(desired_north, -desired_east, old_north, old_east,
                                                            altitude, prev_altitude)

        prev_altitude = altitude
        old_north = desired_north
        old_east = -desired_east

        await drone.offboard.set_velocity_ned(VelocityNedYaw(north_velo, east_velo, alt_velo, 0.0))

        cv2.imshow('Quad Video', norm_frame)

    print("-- Go down 1 m/s, turn to face North")
    await drone.offboard.set_velocity_ned(VelocityNedYaw(0.0, 0.0, 1.0, 0.0))
    await asyncio.sleep(4)

    print("-- Stopping offboard")
    try:
        await drone.offboard.stop()
    except OffboardError as error:
        print(f"Stopping offboard mode failed with error code: \
                  {error._result.result}")


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())
