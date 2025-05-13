from random import random


class Scale:
    def __init__(self, config):
        self.weight = 0
        self.counter = 0

    def zero_and_start(self):
        self.weight = 0

    def read_weight(self, target):
        if self.counter > 20:
            if self.weight < target + 5:
                self.weight += (0.7 * random() + 0.3 * self.weight) / 5
        self.counter += 1
        return self.weight
