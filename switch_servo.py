import uasyncio as asyncio
import machine


class SwitchServo:
    def __init__(self, storage):
        self.ready = storage.get('ready_angle')
        self.pressed = storage.get('pressed_angle')
        self.not_ready = storage.get('not_ready_angle')
        self.servo = machine.PWM(machine.Pin(storage.get('servo_pin')), freq=50)

    def move_servo_to_angle(self, angle):
        angle = max(0, angle % 180)
        duty = int(26 + (angle / 180) * (128 - 26))
        self.servo.duty(duty)

    async def press(self):
        self.move_servo_to_angle(self.pressed)
        await asyncio.sleep(0.200)

    def set_ready(self):
        self.move_servo_to_angle(self.ready)

    def set_not_ready(self):
        self.move_servo_to_angle(self.not_ready)
