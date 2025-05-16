import asyncio
from switch_servo import SwitchServo
from display import Display
from timer import Timer
from scale import Scale


class CoffeeMachine:
    def __init__(self, config, coffee_name, coffee_data):
        self.config = config
        self.measurment_frequency = config.get('measurment_frequency')
        self.weight_graph = []
        self.display = Display(config)
        self.scale = Scale(config)
        self.servo = SwitchServo(config)
        self.servo.set_not_ready()
        self.display.show_coffee(coffee_name, **coffee_data)
        self.is_makeing_coffee = False


    def switch_on(self):
        self.is_makeing_coffee = True

    async def make_coffee(self, extraction_target):
        assert self.is_makeing_coffee
        display_light = asyncio.create_task(self.display.backlight.pulse())
        self.scale.set_zero()
        await self.servo.click(self.servo.set_ready)
        self.weight_graph = []
        timer = Timer()
        counter = 0
        while True:
            extraction_weight = self.scale.read_weight()
            # memory allocation error, in next line:
            if counter % 20 == 0 and len(self.weight_graph) < 20:
                self.weight_graph.append({'x': timer(), 'y': extraction_weight})
            counter += 1
            if extraction_weight >= extraction_target:
                await self.servo.click(self.servo.set_ready)
                break
            await asyncio.sleep(50 / 1000)

        last_extraction_weight = extraction_weight
        while True:
            extraction_weight = self.scale.read_weight()
            if counter % 20 == 0 and len(self.weight_graph) < 20:
                self.weight_graph.append({'x': timer(), 'y': extraction_weight})
            counter += 1
            if not extraction_weight > last_extraction_weight:
                display_light.cancel()
                break
            await asyncio.sleep(.2)
            last_extraction_weight = extraction_weight

        self.servo.set_not_ready()
        self.is_makeing_coffee = False
        print('Coffee made')

    def programm_preinfusion(self, preinfusion_time=20):
        self.servo.press()
        time.sleep(preinfusion_time)
        self.servo.set_ready()
        time.sleep(60)
        self.servo.set_not_ready()
        self.config.set(preinfusion_time)

    def get_chart_json(self):
        data = self.weight_graph.copy()
        self.weight_graph = []
        return {'data': data, 'is_makeing_coffee': self.is_makeing_coffee}
