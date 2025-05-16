import asyncio
import machine # type: ignore


async def monitor_button(gpio_pin_number, coffee_machine, last_time_storage, deepsleeptimer):
    button = machine.Pin(gpio_pin_number, machine.Pin.IN, machine.Pin.PULL_UP)
    last_state = button.value()
    while True:
        state =  button.value()
        if state == 0 and last_state == 1 and not coffee_machine.is_makeing_coffee:
            extraction = last_time_storage.get('extraction')
            coffee_machine.switch_on()
            deepsleeptimer.reset(at_least=180)
            await asyncio.create_task(coffee_machine.make_coffee(extraction))
            deepsleeptimer.reset()
        await asyncio.sleep(90 / 1000)
        last_state = state
