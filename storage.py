try:
    import ujson
except ImportError:
    import json as ujson


class Storage():
    def __init__(self, filename='config.json'):
        self.filename = filename
        with open(self.filename, 'r') as f:
            self._storage = ujson.load(f)

    def get(self, key):
        return self._storage[key]

    def set(self, key, value):
        self._storage[key] = value
        with open(self.filename, 'w') as f:
            ujson.dump(self._storage, f, indent=4)  # Add indentation for pretty-printing
