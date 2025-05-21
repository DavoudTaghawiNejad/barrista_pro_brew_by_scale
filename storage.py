import json


class Storage():
    def __init__(self, filename='config.json'):
        self.filename = filename
        with open(self.filename, 'r') as f:
            self._storage = json.load(f)

    def get(self, key):
        return self._storage[key]

    def set(self, key, value):
        self._storage[key] = value
        with open(self.filename, 'w') as f:
            json.dump(self._storage, f)
