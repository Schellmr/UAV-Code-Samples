import gpiozero
import asyncio
import time

from gpiozero import AngularServo
from gpiozero.pins.pigpio import PiGPIOFactory

from drone_sys import DroneSys as Drone

SER_ADDR = "serial:///dev/serial0:921600"
SIM_ADDR = "udp://:14540"


async def run():
    claw_servo = AngularServo(12, min_angle=0, max_angle=180, min_pulse_width=0.000375, max_pulse_width=0.002,
                              pin_factory=PiGPIOFactory())

    while True:
        print("Opening")
        claw_servo.max()
        time.sleep(3)
        print("Mid")
        claw_servo.mid()
        time.sleep(3)
        print("Closing")
        claw_servo.min()
        time.sleep(3)


if __name__ == '__main__':
    asyncio.ensure_future(run())
    asyncio.get_event_loop().run_forever()
    try:
        while True:
            # do nothing
            time.sleep(.1)
    except KeyboardInterrupt:
        asyncio.get_event_loop().stop()

