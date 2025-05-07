try:
    import ujson
except ImportError:
    import json as ujson

class CoffeeStorage():
    def __init__(self, filename='coffee.json'):
        self.filename = filename
        with open(self.filename, 'r') as f:
            self._storage = ujson.load(f)

    def get_coffees(self):
        return self._storage.get('coffees', [])

    def add_coffee(self, name):
        coffees = self.get_coffees()
        new_coffee = {
            'name': name,
            'dose': 17.0,
            'grind_size': 8,
            'extraction': 40.0
        }
        coffees.append(new_coffee)
        self._storage['coffees'] = coffees
        with open(self.filename, 'w') as f:
            ujson.dump(self._storage, f, indent=4)  # Add indentation for pretty-printing
        return True

    def update_coffee(self, name, dose=None, grind_size=None, extraction=None):
        coffees = self.get_coffees()
        for coffee in coffees:
            if coffee['name'] == name:
                if dose is not None:
                    coffee['dose'] = round(float(dose), 1)
                if grind_size is not None:
                    coffee['grind_size'] = int(grind_size)
                if extraction is not None:
                    coffee['extraction'] = round(float(extraction), 1)
                with open(self.filename, 'w') as f:
                    ujson.dump(self._storage, f, indent=4)  # Add indentation for pretty-printing
                return True
        return False
