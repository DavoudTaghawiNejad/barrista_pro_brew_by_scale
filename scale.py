import json
from hx711 import HX711




class Scale:
    def __init__(self, config):
        self.hx = HX711(d_out=config.get('scale')['dt'], pd_sck=config.get('scale')['sck'])
        self.scale_factor = config.get('scale_factor')
        self.zero = None
        self.weight_graph = []

    def average_raw_reading(self, num):
        return sum([self.hx.read() for _ in range(num)]) / num

    def set_zero(self, repetitions=20):
        self.zero = self.average_raw_reading(repetitions)

    def set_scale(self, repetitions=50):
        self.set_zero(repetitions)
        print('Enter known_weight:')
        known_weight = float(input())
        self.scale_factor = (self.average_raw_reading(repetitions) - self.zero) / known_weight
        print(f'{self.scale_factor=}')

    def read_weight(self):
        reading = (self.hx.read() - self.zero) / self.scale_factor
        return reading
