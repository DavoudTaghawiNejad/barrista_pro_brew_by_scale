import asyncio
import time
from random import random
import json


class CoffeeMachine:
    def __init__(self, config):
        self.storage = config
        self.measurment_frequency = config.get('measurment_frequency')
        self.extraction = self.storage.get('extraction')
        self.weight_graph = []

    async def make_coffee(self):
        self.weight_graph = []
        print('scale.zero_and_start')
        print('servo.press')
        print('servo.ready')
        extraction_weight = 0
        while True:
            extraction_weight += random() / 60 * 5

            self.weight_graph.append(extraction_weight)
            print(extraction_weight)

            if extraction_weight >= self.extraction:
                print('servo.press')
                print('servo.not_ready')
                break
            await asyncio.sleep(10 / 1000)

    def programm_preinfusion(self, preinfusion=20):
        print('servo.press')
        time.sleep(preinfusion)
        print('servo.ready')
        time.sleep(60)
        print('servo.set_not_ready')
        self.storage.set(preinfusion)

    def get_chart_json(self):
        return json.dumps(self.weight_graph)
