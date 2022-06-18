import asyncio
import mavsdk_gets

from drone_sys import DroneSys


async def run():
    drone = DroneSys()

    await drone.connect(system_address="udp://:14540")
    asyncio.ensure_future(mavsdk_gets.get_telemetry(drone))
    asyncio.ensure_future(mavsdk_gets.get_altitude(drone))
    asyncio.ensure_future(mavsdk_gets.get_video(drone))
    print("Telem listeners and video started.")

    asyncio.ensure_future(mavsdk_gets.set_descent(drone))

if __name__ == '__main__':
    asyncio.ensure_future(run())
    asyncio.get_event_loop().run_forever()
