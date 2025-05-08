import json
from hx711 import HX711

class Scale:
    def __init__(self, config):
        self.hx = HX711(d_out=4, pd_sck=5)  # DT to GPIO 4, SCK to GPIO 5
        self.scale_factor = config.get('scale_factor')
        self.zero = None
        self.weight_graph = []

    def zero_and_start(self):
        while True:
            self.zero = self.hx.read()
            self.weight_graph = []
            if -0.05 < self.hx.get_units() - self.zero < 0.05:
                break

    def read_weight(self):
        reading = (self.hx.read() - self.zero) / self.scale_factor
        self.weight_graph.append(reading)  # Add newest
        return reading

    def get_chart_json(self):
        return json.dumps(self.weight_graph)
