import asyncio

from mavsdk import System
from mavsdk.offboard import (OffboardError, VelocityNedYaw)
import random

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

    i = 0
    while i < 100:
        i += 1
        print("Moving")
        await asyncio.sleep(0.05)
        await drone.offboard.set_velocity_ned(VelocityNedYaw(random.uniform(-1, 1), 0.0, 0.0, 0.0))

    await drone.offboard.set_velocity_ned(VelocityNedYaw(1, 0.0, 0.0, 0.0))
    await asyncio.sleep(3)
    await drone.offboard.set_velocity_ned(VelocityNedYaw(-1, 0.0, 0.0, 0.0))
    await asyncio.sleep(3)

    print("-- Stopping offboard")
    try:
        await drone.offboard.stop()
    except OffboardError as error:
        print(f"Stopping offboard mode failed with error code: \
              {error._result.result}")


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())