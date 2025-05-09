import asyncio
from random import random
import time


class Timer:
    def __init__(self):
        self.start_time = time.ticks_ms()

    def __call__(self):
        return (time.ticks_ms() - self.start_time) / 1000


class CoffeeMachine:
    def __init__(self, config):
        self.config = config
        self.measurment_frequency = config.get('measurment_frequency')
        self.weight_graph = []
        self.is_makeing_coffee = False

    def switch_on(self):
        self.is_makeing_coffee = True

    async def make_coffee(self, extraction):
        assert self.is_makeing_coffee
        extraction_weight = 0
        self.weight_graph = []
        print('Start coffee making')
        print('scale.zero_and_start')
        print('servo.press')
        print('servo.ready')
        extraction_weight = 0
        counter = 0
        timer = Timer()
        while True:
            if timer() > 1:
                extraction_weight += (0.7 * random() + 0.3 * extraction_weight) / 60 * 5

            if counter % 5 == 0:
                self.weight_graph.append({'x': timer(), 'y': extraction_weight})
                print(timer(), extraction_weight)

            if extraction_weight >= extraction:
                print('servo.press')
                print('servo.not_ready')
                break
            await asyncio.sleep(10 / 1000)
            counter += 1
        self.weight_graph = []
        self.is_makeing_coffee = False
        print('Coffee made')

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
        return {'data': data, 'is_makeing_coffee': self.is_makeing_coffee}
