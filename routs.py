import asyncio
import webrepl
import json
import machine # type: ignore
from microdot import Microdot, Response
from storage import Storage
from coffee_machine import CoffeeMachine
from coffee_storage import CoffeeStorage
from tools import load_html_generatory
from reset_cause import substitute_coffee_name_with_reset_cause


configuration = Storage(filename='config.json')
coffee_storage = CoffeeStorage(filename='coffee.json')
last_time_storage = Storage(filename='last_time.json')
current_coffee = last_time_storage.get('last_brewed')
current_coffee_data = coffee_storage.get_coffee(current_coffee)
current_coffee = substitute_coffee_name_with_reset_cause(current_coffee)
coffee_machine = CoffeeMachine(configuration,
                               current_coffee,
                               current_coffee_data)


app = Microdot()


@app.route('/')
async def index(request):
    html = load_html_generatory('webpage.html')
    return Response(html, headers={'Content-Type': 'text/html'})

@app.route('/get_chart_data')
async def get_chart_data(request):
    chart_data = coffee_machine.get_chart_json()
    return json.dumps(chart_data), 200, {'Content-Type': 'application/json'}

@app.route('/update', methods=['POST'])
async def update(request):
    try:
        data = request.json
        last_time_storage.set('extraction', round(float(data['extraction']), 1))  # remember extraction for button operation
        return {'status': 'success'}, 200
    except (KeyError, ValueError):
        return {'status': 'error', 'message': 'Invalid data'}, 400

@app.route('/make_coffee', methods=['POST'])
async def make_coffee(request):
    if coffee_machine.is_makeing_coffee:  # Assuming is_brewing is a method or attribute to check status
        return {'status': 'error', 'message': 'Coffee is already being made'}, 400
    try:
        data = request.json
        print(data['extraction'])
        try:
            extraction = round(float(data['extraction']), 1)
        except ValueError:
            extraction = last_time_storage.get('extraction')
        coffee_machine.switch_on()
        asyncio.create_task(coffee_machine.make_coffee(extraction))
        coffee_name = data.get('name')
        if coffee_name:
            last_time_storage.set('last_brewed', coffee_name)
        return {'status': 'success'}, 200
    except (KeyError, ValueError) as e:
        return {'status': 'error', 'message': f'{str(e)}'}, 400

@app.route('/add_coffee', methods=['POST'])
async def add_coffee(request):
    try:
        data = request.json
        name = data.get('name')
        dose = data.get('dose')
        grind_size = data.get('grind_size')
        extraction = data.get('extraction')
        if name and dose is not None and grind_size is not None and extraction is not None:
            coffee_storage.add_coffee(name, dose, grind_size, extraction)
            return {'status': 'success'}, 200
        else:
            return {'status': 'error', 'message': 'Missing required parameters'}, 400
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
        success = coffee_storage.update_coffee(name, dose, grind_size, extraction)
        if success:
            return {'status': 'success'}, 200
        else:
            return {'status': 'error', 'message': 'Coffee not found'}, 404
    except Exception as e:
        print(e)
        return {'status': 'error', 'message': str(e)}, 400

@app.route('/get_last_brewed')
async def get_last_brewed(request):

    last_brewed = last_time_storage.get('last_brewed')
    print("LAST COFFE REQUESTED")
    print(last_brewed)
    return {'last_brewed': last_brewed}, 200, {'Content-Type': 'application/json'}


@app.route('/get_coffee_names', methods=['GET'])
async def get_coffee_names(request):
    coffees = coffee_storage.get_coffee_names()
    print(f'{coffees=}')
    return {'names': coffees}, 200, {'Content-Type': 'application/json'}

@app.route('/get_coffee', methods=['GET'])
async def get_coffee(request):
    name = request.args.get('name')
    if name:
        coffee = coffee_storage.get_coffee(name)
        print(f'{coffee=}')

        return {'coffee': coffee}, 200, {'Content-Type': 'application/json'}
    else:
        return {'status': 'error', 'message': 'Name parameter is required'}, 400


@app.route('/update_display', methods=['POST'])
async def update_display(request):
    try:
        data = request.json
        coffee_name = data.get('name', 'Unknown')
        dose = data.get('dose')
        grind_size = data.get('grind_size')
        extraction = data.get('extraction')

        coffee_machine.display.show_coffee(coffee_name, dose, grind_size, extraction)

        return {'status': 'success'}, 200
    except Exception as e:
        return {'status': 'error', 'message': str(e)}, 400

@app.route('/start_webrepl', methods=['POST'])
async def start_webrepl(request):
    try:
        webrepl.start()
        return {'status': 'success'}, 200
    except Exception as e:
        return {'status': 'error', 'message': str(e)}, 400

@app.route('/config')
async def config(request):
    return Response(load_html_generatory('config.html'), headers={'Content-Type': 'text/html'})

@app.route('/get_config')
async def get_config(request):
    config_data = configuration._storage
    return config_data, 200, {'Content-Type': 'application/json'}

@app.route('/reset_esp32', methods=['POST'])
async def reset_esp32(request):
    try:
        print('start reset...')
        machine.reset()
        print('... failed to reset')
        return {'status': 'error', 'message': 'Failed to reset'}, 500

    except Exception as e:
        return {'status': 'error', 'message': f'Did not reset: {e}'}, 400

@app.route('/save_config', methods=['POST'])
async def save_config(request):
    data = request.json
    try:

        json.dumps(data) # Validate JSON using json.loads, will raise an error if data is not serializable to JSON
    except Exception as e:
        return {'status': 'error', 'message': 'JSON validation error'}, 400
    try:
        configuration._storage = data
        with open(configuration.filename, 'w') as f:
            json.dump(configuration._storage, f)
        return {'status': 'success'}, 200
    except Exception as e:
        return {'status': 'error', 'message': str(e)}, 400
