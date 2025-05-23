from microdot import Microdot, Response
try:
    import ujson
    import uasyncio as asyncio
    from scale import read_load_cell, update_data
    from network_tools import connect_wifi
    from coffee_machine import CoffeeMachine
    PORT = 80
    HOST = '0.0.0.0'
except ImportError:
    from fake_coffee_machine import CoffeeMachine
    connect_wifi = lambda : None
    import json as ujson
    import asyncio
    PORT = 5008
    HOST = 'localhost'
print("Imports successful")  # Debug print after imports

from storage import Storage
from coffee_storage import CoffeeStorage  # Keep the import

with open('webpage.html', 'r') as f:
    HTML = f.read()

app = Microdot()

config = Storage(filename='config.json')
coffee_storage = CoffeeStorage(filename='coffee.json')
coffee_machine = CoffeeMachine(config)

@app.route('/')
async def index(request):
    chart_data = coffee_machine.get_chart_json()
    extraction = str(config.get('extraction'))
    html = HTML.replace('{{chart_data}}', str(chart_data))
    html = html.replace('{{extraction}}', str(int(float(extraction))))
    return Response(html, headers={'Content-Type': 'text/html'})

@app.route('/get_chart_data')
async def get_chart_data(request):
    chart_data = coffee_machine.get_chart_json()
    return chart_data, 200, {'Content-Type': 'application/json'}

@app.route('/update', methods=['POST'])
async def update(request):
    try:
        data = request.json
        config.set('extraction', round(float(data['extraction']), 1))
        return {'status': 'success'}, 200
    except (KeyError, ValueError):
        return {'status': 'error', 'message': 'Invalid data'}, 400

@app.route('/make_coffee', methods=['POST'])
async def make_coffee(request):
    try:
        data = request.json
        extraction = round(float(data['extraction']), 1)
        await coffee_machine.make_coffee(extraction)
        return {'status': 'success'}, 200
    except (KeyError, ValueError):
        return {'status': 'error', 'message': 'Invalid data'}, 400

# Update routes to use coffee_storage
@app.route('/get_coffees', methods=['GET'])
async def get_coffees(request):
    coffees = coffee_storage.get_coffees()
    return {'coffees': coffees}, 200, {'Content-Type': 'application/json'}

@app.route('/add_coffee', methods=['POST'])
async def add_coffee(request):
    try:
        data = request.json
        name = data.get('name')
        if not name:
            return {'status': 'error', 'message': 'Name is required'}, 400
        coffee_storage.add_coffee(name)
        return {'status': 'success'}, 200
    except Exception as e:
        return {'status': 'error', 'message': str(e)}, 400

@app.route('/update_coffee', methods=['POST'])
async def update_coffee(request):
    try:
        data = request.json
        name = data.get('name')
        dose = data.get('dose')
        grind_size = data.get('grind_size')
        extraction = data.get('extraction')
        if not name:
            return {'status': 'error', 'message': 'Name is required'}, 400
        success = coffee_storage.update_coffee(name, dose, grind_size, extraction)
        if success:
            return {'status': 'success'}, 200
        else:
            return {'status': 'error', 'message': 'Coffee not found'}, 404
    except Exception as e:
        return {'status': 'error', 'message': str(e)}, 400

async def main():
    try:
        connect_wifi()
        print(f'http://{HOST}:{PORT}')
        await app.start_server(HOST, port=PORT)
        print('andhere')
    except Exception as e:
        print(f"Error starting server: {e}")
        import sys
        sys.exit(1)

asyncio.run(main())
