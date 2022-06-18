import asyncio
import time

from drone_sys import DroneSys as Drone

SER_ADDR = "serial:///dev/serial0:921600"
SIM_ADDR = "udp://:14540"


async def run():
    drone = Drone()

    await drone.connect(system_address=SER_ADDR)

    print("Connection Made")
    asyncio.ensure_future(drone.get_attitude())
    asyncio.ensure_future(drone.get_altitude())
    asyncio.ensure_future(drone.get_pi_video(save_video=True))
    print("listeners and video started.")

    asyncio.ensure_future(drone.print_ui())
    asyncio.ensure_future(drone.set_velocities(drone, adaptive=True))


if __name__ == '__main__':
    asyncio.ensure_future(run())
    asyncio.get_event_loop().run_forever()
    try:
        while True:
            # do nothing
            time.sleep(.1)
    except KeyboardInterrupt:
        asyncio.get_event_loop().stop()
