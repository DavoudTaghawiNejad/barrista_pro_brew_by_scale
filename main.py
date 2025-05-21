import sys
import io
import gc
import asyncio
import webrepl
from deepsleep import DeepSleepTimer
from microdot import Microdot
from network_tools import Wifi
from button import monitor_button
from storage import Storage
from routs import coffee_machine, last_time_storage


LAST_ERROR = None

try:
    configuration = Storage(filename='config.json')

    gc.collect()

    wifi = Wifi(configuration)
    gc.collect()
    deepsleeptimer = DeepSleepTimer(configuration,
                                    coffee_machine=coffee_machine)

    app = Microdot()


    @app.before_request
    def before_request_reset_timer(request):
        deepsleeptimer.reset()


    @app.after_request
    def after_request_reset_timer(request, response):
        deepsleeptimer.reset()


    async def main_loop():
        button = asyncio.create_task(monitor_button(configuration.get('make_coffee_button'),
                                    coffee_machine, last_time_storage, deepsleeptimer=deepsleeptimer))

        await wifi.display_credentials_until_connected(display=coffee_machine.display)

        from routs import app as subapp
        app.mount(subapp)
        server = app.start_server(port=80, debug=True)
        deep_sleep_check = asyncio.create_task(deepsleeptimer.check_and_sleep())
        await asyncio.gather(server, button, deep_sleep_check)


    asyncio.run(main_loop())
except Exception as e:
    webrepl.start()
    error_stream = io.StringIO()
    sys.print_exception(e, error_stream)
    LAST_ERROR = f"Type: {type(e).__name__}\nMessage: {str(e)}\nTraceback:\n{error_stream.getvalue()}"
    last_time_storage.set('last_error', LAST_ERROR)
    raise
