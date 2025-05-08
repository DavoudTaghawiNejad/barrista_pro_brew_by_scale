import json


class CoffeeStorage():
    def __init__(self, filename='coffee.json'):
        self.filename = filename
        with open(self.filename, 'r') as f:
            self._storage = json.load(f)

    def get_coffee_names(self):
        return list(self._storage.keys())

    def get_coffee(self, name):
        return self._storage[name]

    def add_coffee(self, name, dose, grind_size, extraction):
        self.update_coffee(name, dose=dose, grind_size=grind_size, extraction=extraction)

    def update_coffee(self, name, dose=None, grind_size=None, extraction=None):
        self._storage[name] = {'dose': dose,
                               'grind_size': grind_size,
                               'extraction': extraction}
        with open(self.filename, 'w') as f:
            json.dump(self._storage, f)
