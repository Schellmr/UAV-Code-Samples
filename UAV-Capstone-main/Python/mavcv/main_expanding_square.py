import asyncio

from mavsdk import System
from mavsdk.offboard import (OffboardError, PositionNedYaw)
from util.expanding_square import expanding_square


async def run():
    waypoints = expanding_square(5, 30)
    print(waypoints)

    """ Does Offboard control using position NED coordinates. """

    drone = System()
    await drone.connect(system_address="udp://:14540")

    print("-- Arming")
    await drone.action.arm()

    print("-- Setting initial setpoint")
    await drone.offboard.set_position_ned(PositionNedYaw(0.0, 0.0, 0.0, 0.0))

    print("-- Starting offboard")
    try:
        await drone.offboard.start()
    except OffboardError as error:
        print(f"Starting offboard mode failed with error code: {error._result.result}")
        print("-- Disarming")
        await drone.action.disarm()
        return

    print("-- Ascend to search height")
    await drone.offboard.set_position_ned(PositionNedYaw(0.0, 0.0, -20.0, 0.0))
    await asyncio.sleep(5)

    for waypoint in waypoints:
        print("-- Go " + str(waypoint[0]) + "m North, " + str(waypoint[1]) + "m East, 0m Down within local " +
              "coordinate system, turn to face South")
        await drone.offboard.set_position_ned(PositionNedYaw(waypoint[0], waypoint[1], -20.0, 0.0))
        await asyncio.sleep(5)

    print("-- Stopping offboard")
    try:
        await drone.offboard.stop()
    except OffboardError as error:
        print(f"Stopping offboard mode failed with error code: {error._result.result}")


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())
