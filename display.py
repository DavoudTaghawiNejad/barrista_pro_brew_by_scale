import asyncio
from machine import Pin, SPI, PWM
import pcd8544

class Display():
    def __init__(self, config):
        display = config.get('display')
        spi = SPI(1)
        spi.init(baudrate=2000000, polarity=0, phase=0)
        self.bl = PWM(Pin(display['bl'], Pin.OUT, value=1), freq=5000)
        self.display = pcd8544.PCD8544_FRAMEBUF(spi=spi,
                                                cs=Pin(display['cs']),
                                                dc=Pin(display['dc']),
                                                rst=Pin(display['rst']))

    async def pulse(self):
        delay = .075
        step = 25
        while True:
            for brightness in range(0, 900 - step, step):
                self.bl.duty(brightness)
                await asyncio.sleep(delay)

            for brightness in range(900, step, -step):
                self.bl.duty(brightness)
                await asyncio.sleep(delay)
