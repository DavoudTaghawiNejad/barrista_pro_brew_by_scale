import ujson
from hx711 import HX711

class Scale:
    def __init__(self, scale_factor):
        self.hx = HX711(dout=4, pd_sck=5)  # DT to GPIO 4, SCK to GPIO 5
        self.hx.set_scale(scale_factor)
        self.weight_graph = []

    def zero_and_start(self):
        while True:
            self.hx.tare(times=15)
            self.weight_graph = []
            if -0.05 < self.hx.get_units() < 0.05:
                break

    def read_weight(self):
        reading = self.hx.get_units()
        self.weight_graph.append(reading)  # Add newest
        return reading

    def get_chart_json(self):
        return ujson.dumps(self.weight_graph)
