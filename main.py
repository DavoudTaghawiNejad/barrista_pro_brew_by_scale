
import gc
import asyncio
from microdot import Microdot
from network_tools import connect_wifi, wifi_credentials_until_wifi_is_on
from button import monitor_button
from storage import Storage
from routs import coffee_machine, last_time_storage


configuration = Storage(filename='config.json')

gc.collect()

wifi_connected = connect_wifi(configuration.get('wifi_name'),
                              configuration.get('wifi_password'))
gc.collect()


app = Microdot()


async def main():
    button = asyncio.create_task(monitor_button(configuration.get('make_coffee_button'),
                                 coffee_machine, last_time_storage))

    await wifi_credentials_until_wifi_is_on(ssid=configuration.get('wifi_name'),
                                            password=configuration.get('wifi_password'),
                                            display=coffee_machine.display)

    from routs import app as subapp
    app.mount(subapp)
    server = app.start_server(debug=True)
    await asyncio.gather(server, button)

asyncio.run(main())
