import esp32 # type: ignore
import machine # type: ignore
import time
import asyncio


class DeepSleepTimer:
    def __init__(self, config, coffee_machine):
        self.coffee_machine = coffee_machine
        self.sleep_time_ms = config.get('deepsleep_after_seconds') * 1000
        self.next_sleep = time.ticks_ms() + self.sleep_time_ms
        self.reset()
        self.pins = config.get('wake_up_buttons')

    def reset(self, at_least_seconds=0):
        sleep_time_ms = max(at_least_seconds * 1000, self.sleep_time_ms)
        self.next_sleep = max(time.ticks_ms() + sleep_time_ms, self.next_sleep)

    async def check_and_sleep(self):
        while True:
            if time.ticks_ms() >= self.next_sleep:
                self.coffee_machine.display.power_off()
                self.coffee_machine.display.backlight.off_for_deepsleep()
                buttons = [machine.Pin(pin, machine.Pin.IN, machine.Pin.PULL_UP)
                           for pin in self.pins]
                esp32.wake_on_ext1(pins=buttons,level=esp32.WAKEUP_ALL_LOW)
                machine.deepsleep()
            await asyncio.sleep(1)
