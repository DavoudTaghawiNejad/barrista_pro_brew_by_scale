import uasyncio as asyncio
import utime as time
from switch_servo import SwitchServo
from scale import Scale

class CoffeeMachine:
    def __init__(self, config):
        self.config = config
        self.measurment_frequency = config.get('measurment_frequency')
        self.servo = SwitchServo()
        self.servo.set_not_ready()
        self.scale = Scale()

    async def make_coffee(self):
        self.scale.zero_and_start()
        self.servo.press()
        self.servo.set_ready()
        while True:
            extraction_weight = self.scale.read_weight()
            if extraction_weight >= self.config.get('extraction'):
                self.servo.press()
                self.servo.set_not_ready()
                break
            await asyncio.sleep(10 / 1000)

    def programm_preinfusion(self, preinfusion_time=20):
        self.servo.press()
        time.sleep(preinfusion_time)
        self.servo.set_ready()
        time.sleep(60)
        self.servo.set_not_ready()
        self.config.set(preinfusion_time)

    def get_chart_json(self):
        self.scale.get_chart_json(self)
