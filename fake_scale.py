from random import random


class Scale:
    def __init__(self, config):
        self.weight = 0
        self.counter = 0

    def set_zero(self, _=None):
        self.weight = 0

    def set_scale(self, _=None):
        self.zero()
        self.scale_factor = 1

    def read_weight(self, target=40):
        if self.counter > 20:
            if self.weight < target + 5:
                self.weight += (0.7 * random() + 0.3 * self.weight) / 5
        self.counter += 1
        return self.weight
