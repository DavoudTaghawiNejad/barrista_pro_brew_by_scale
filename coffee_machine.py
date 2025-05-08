import json
import asyncio
import time
from switch_servo import SwitchServo
from scale import Scale

class CoffeeMachine:
    def __init__(self, config):
        self.config = config
        self.measurment_frequency = config.get('measurment_frequency')
        self.servo = SwitchServo(config)
        self.servo.set_not_ready()
        self.scale = Scale(config)

    async def make_coffee(self, extraction):
        self.scale.zero_and_start()
        self.servo.click(self.servo.set_ready)
        self.weight_graph = []
        time = 0
        while True:
            extraction_weight = self.scale.read_weight()

            if time % 10 == 0:
                self.weight_graph.append(extraction_weight)

            if extraction_weight >= extraction:
                self.servo.click(self.servo.set_not_ready)
                break
            await asyncio.sleep(10 / 1000)
            time += 1

    def programm_preinfusion(self, preinfusion_time=20):
        self.servo.press()
        time.sleep(preinfusion_time)
        self.servo.set_ready()
        time.sleep(60)
        self.servo.set_not_ready()
        self.config.set(preinfusion_time)

    def get_chart_json(self):
        data = self.weight_graph.copy()
        self.weight_graph = []
        return json.dumps(data)
