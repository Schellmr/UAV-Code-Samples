import asyncio
from mavsdk import System
from mavsdk.offboard import VelocityNedYaw, OffboardError
from util.cv_container import CVStuff


async def get_altitude(drone):
    """ Prints the altitude when it changes """

    async for position in drone.telemetry.position():
        await asyncio.sleep(0.01)
        return position.relative_altitude_m


async def get_attitude(drone):
    """ Prints the flight mode when it changes """

    async for msg in drone.telemetry.attitude_euler():
        await asyncio.sleep(0.01)
        return msg.pitch_deg, msg.roll_deg, msg.yaw_deg


async def run():
    drone = System()
    image = CVStuff()

    await drone.connect(system_address="udp://:14540")

    print("Waiting for drone to connect...")
    async for state in drone.core.connection_state():
        if state.is_connected:
            print(f"Drone discovered!")
            break

    await drone.offboard.set_velocity_ned(VelocityNedYaw(0, 0, 0, 0))

    try:
        await drone.offboard.start()
    except OffboardError as error:
        print(f"Starting offboard mode failed with error code: \
                  {error._result.result}")
        print("-- Disarming")
        await drone.action.disarm()
        return

    while True:
        attitude_stuff, altitude_stuff = await asyncio.gather(get_attitude(drone), get_altitude(drone))
        north, east, _, _ = image.find_velos(attitude_stuff[0], attitude_stuff[1], altitude_stuff)
        # print(attitude_stuff)
        # print(altitude_stuff)
        await drone.offboard.set_velocity_ned(VelocityNedYaw(north, east, 0, 0))
        await asyncio.sleep(0.1)


if __name__ == "__main__":
    # a = asyncio.get_event_loop().run_until_complete(run())
    loop = asyncio.get_event_loop()
    # loop.run_until_complete(run())
    loop.create_task(run())
    loop.run_forever()


