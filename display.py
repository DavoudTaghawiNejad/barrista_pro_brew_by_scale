import asyncio
from machine import Pin, SPI  # type: ignore
import pcd8544
from backlight import Backlight


class Display():
    def __init__(self, config):
        display = config.get('display')
        spi = SPI(display['spi'])
        spi.init(baudrate=2000000, polarity=0, phase=0, sck=Pin(display['sck']), mosi=Pin(display['mosi']))
        self.backlight = Backlight(display['bl'])
        self.display = pcd8544.PCD8544_FRAMEBUF(spi=spi,
                                                cs=Pin(display['cs']),
                                                dc=Pin(display['dc']),
                                                rst=Pin(display['rst']))

    def show_coffee(self, coffee_name, dose, grind_size, extraction):
        self.display.fill(0)
        self.display.text(coffee_name.replace('The ', '').replace('the ', ''), 0, 0, 1)
        self.display.hline(0, 10, 83)
        self.display.text(f'Dose: {dose}', 0, 14, 1)
        self.display.text(f'Grind: {grind_size}', 0, 26, 1)
        self.display.text(f'Coffee: {extraction}', 0, 38, 1)
        self.display.show()

    def show_text(self, text, inverted=False):
        text = text.split('\n')
        rows  = len(text)
        line_size = 48 // rows
        self.display.fill(inverted)
        for line_number, line in enumerate(text):
            self.display.text(line, 0, line_size * line_number, not inverted)
        self.display.show()

    async def show_text_timed(self, text, sleep1=5, sleep2=20, inverted=False):
        previous_on_screen = self.display.buf[:]
        self.show_text(text, inverted=inverted)
        await asyncio.sleep(sleep1)
        self.display.data(previous_on_screen)
        await asyncio.sleep(sleep2)


    def power_off(self):
        self.display.power_off()
        self.backlight.off()
