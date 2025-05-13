import time


class Timer:
    def __init__(self):
        self.start_time = time.ticks_ms()

    def __call__(self):
        return (time.ticks_ms() - self.start_time) / 1000
