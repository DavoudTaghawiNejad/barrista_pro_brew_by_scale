from math import ceil
import asyncio
from machine import Pin, PWM # type: ignore


class Backlight():
    def __init__(self, backlight_pin):
        self.pin_number = backlight_pin
        self.bl = PWM(Pin(backlight_pin, Pin.OUT, value=1), freq=5000)
        self.intensity = 1
        self.set_intensity(1)
        self.suspended = False

    def set_intensity(self, intensity):
        assert intensity <= 1
        self.bl.duty(int(intensity * 1023))
        self.intensity = intensity

    def suspend(self):
        self.bl.duty(0)
        self.suspended = True

    def revive(self):
        self.set_intensity(self.intensity)
        #asyncio.run(self.fade_in(delay = .075, step = 25, start=0, target=self.intensity))
        self.suspended = False

    def on(self):
        self.set_intensity(1)

    def off(self):
        self.set_intensity(0)

    def off_for_deepsleep(self):
        Pin(self.pin_number, Pin.IN, Pin.PULL_DOWN)


    async def fade_in(self, delay=1 / 20, steps=20, max=1):
        min = int(self.intensity * 1000)
        max = int(max * 1000)
        step = int(ceil(1000 / 20))
        for brightness_pct in range(min, max, step):
            self.set_intensity(brightness_pct / 1000)
            await asyncio.sleep(delay)

    async def fade_out(self, delay=1 / 20, steps=20, min=0):
        min = int(min * 1000)
        max = int(self.intensity * 1000)
        step = -int(ceil(1000 / 20))
        for brightness_pct in range(max, min, step):
            self.set_intensity(brightness_pct / 1000)
            await asyncio.sleep(delay)

    async def pulse(self):
        try:
            delay = 1 / 20
            steps = 20
            while True:
                await self.fade_out(delay, steps, min=0.1)
                await self.fade_in(delay, steps, max=0.9)
        except asyncio.CancelledError:
             self.fade_in(delay, steps, max=1)
