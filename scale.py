import json
from hx711 import HX711




class Scale:
    def __init__(self, config):
        self.hx = HX711(d_out=config.get('scale')['dt'], pd_sck=config.get('scale')['sck'])
        self.config = config
        self.scale_factor = config.get('scale_factor')
        self.zero = None
        self.weight_graph = []

    def average_raw_reading(self, num):
        return sum([self.hx.read() for _ in range(num)]) / num

    def set_zero(self, repetitions=20):
        self.zero = self.average_raw_reading(repetitions)

    def set_scale(self, known_weight, repetitions=20):
        self.previous_scale_factor = self.scale_factor
        self.scale_factor = (
            self.average_raw_reading(repetitions) - self.zero) / known_weight

    def save_scale_factor(self):
        self.config.set('scale_factor', self.scale_factor)

    def reset_scale_factor(self):
        self.scale_factor = self.config.get('scale_factor')

    def read_weight(self):
        reading = (self.hx.read() - self.zero) / self.scale_factor
        return reading
