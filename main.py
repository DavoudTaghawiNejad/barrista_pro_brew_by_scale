from microdot import Microdot, Response
from network_tools import connect_wifi
from fake_coffee_machine import CoffeeMachine
from storage import Storage
from coffee_storage import CoffeeStorage


with open('webpage.html', 'r') as f:
    HTML = f.read()

app = Microdot()

config = Storage(filename='config.json')
coffee_storage = CoffeeStorage(filename='coffee.json')
coffee_machine = CoffeeMachine(config)
last_time_storage = Storage(filename='last_time.json')


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

        # Save the last brewed coffee
        coffee_name = data.get('name')  # Assuming the name is sent in the request
        if coffee_name:
            last_time_storage.set('last_brewed', coffee_name)

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

@app.route('/get_last_brewed')
async def get_last_brewed(request):

    last_brewed = last_time_storage.get('last_brewed')
    print("LAST COFFE REQUESTED")
    print(last_brewed)
    return {'last_brewed': last_brewed}, 200, {'Content-Type': 'application/json'}


connect_wifi('ANDREIA-2G', '12341234')
app.run(debug=True)
