import asyncio
import time
from random import random
import json


class CoffeeMachine:
    def __init__(self, config):
        self.config = config
        self.measurment_frequency = config.get('measurment_frequency')
        self.weight_graph = []
        self.is_brewing = False

    async def make_coffee(self, extraction):
        self.is_brewing = True
        extraction_weight = 0
        self.weight_graph = []
        print('scale.zero_and_start')
        print('servo.press')
        print('servo.ready')
        extraction_weight = 0
        time = 0
        while True:
            if time > 100:
                extraction_weight += (0.7 * random() / 60 * 5 + 0.3 * extraction_weight)

            if time % 10 == 0:
                self.weight_graph.append(extraction_weight)

            if extraction_weight >= extraction:
                print('servo.press')
                print('servo.not_ready')
                break
            await asyncio.sleep(10 / 1000)
            time += 1
        self.is_brewing = False

    def programm_preinfusion(self, preinfusion=20):
        print('servo.press')
        time.sleep(preinfusion)
        print('servo.ready')
        time.sleep(60)
        print('servo.set_not_ready')
        self.config.set(preinfusion)

    def get_chart_json(self):
        data = self.weight_graph.copy()
        self.weight_graph = []
        return json.dumps(data)
