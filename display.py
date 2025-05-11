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

    def show_coffee(self, coffee_name, dose, grind_size, extraction):
        self.display.fill(0)
        self.display.text(coffee_name.replace('The ', '').replace('the ', ''), 0, 0, 1)
        self.display.hline(0, 10, 83)
        self.display.text(f'Dose: {dose}', 0, 14, 1)
        self.display.text(f'Grind: {grind_size}', 0, 26, 1)
        self.display.text(f'Coffee: {extraction}', 0, 38, 1)

        self.display.show()
