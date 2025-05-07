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
    PORT = 5007
    HOST = 'localhost'
print("Imports successful")  # Debug print after imports

from storage import Storage

with open('webpage.html', 'r') as f:
    HTML = f.read()

app = Microdot()

config = Storage(filename='config.json')
coffee_machine = CoffeeMachine(config)

@app.route('/')
async def index(request):
    chart_data = coffee_machine.get_chart_json()
    preinfusion = str(config.get('preinfusion'))
    extraction = str(config.get('extraction'))
    servo_angle = str(config.get('servo_angle'))
    print(f"Chart data: {chart_data}")  # Debug print
    print(f"Preinfusion: {preinfusion}")  # Debug print
    print(f"Extraction: {extraction}")  # Debug print
    print(f"Servo angle: {servo_angle}")  # Debug print
    html = HTML.replace('{{chart_data}}', str(chart_data))  # Ensure string for replacement
    html = html.replace('{{preinfusion}}', preinfusion)
    html = html.replace('{{extraction}}', extraction)
    html = html.replace('{{servo_angle}}', servo_angle)
    print(f"Generated HTML length: {len(html)}")  # Debug print for HTML length
    return Response(html, headers={'Content-Type': 'text/html'})

@app.route('/get_chart_data')
async def get_chart_data(request):
    chart_data = coffee_machine.get_chart_json()
    return chart_data, 200, {'Content-Type': 'application/json'}

@app.route('/update', methods=['POST'])
async def update(request):
    try:
        data = request.ujson
        config.set('extraction', round(float(data['extraction']), 1))
        return {'status': 'success'}, 200
    except (KeyError, ValueError):
        return {'status': 'error', 'message': 'Invalid data'}, 400

@app.route('/make_coffee', methods=['POST'])
async def make_coffee(request):
    try:
        data = request.json  # Assuming JSON parsing
        extraction = round(float(data['extraction']), 1)
        config.set('extraction', extraction)  # Same as /update
        await coffee_machine.make_coffee(extraction)  # Proceed after update
        return {'status': 'success'}, 200
    except (KeyError, ValueError):
        return {'status': 'error', 'message': 'Invalid data'}, 400

async def main():
    try:
        connect_wifi()
        print('here')
        await app.start_server(HOST, port=PORT, debug=True)
        print('andhere')
    except Exception as e:
        print(f"Error starting server: {e}")
        import sys
        sys.exit(1)

asyncio.run(main())
