import asyncio
import machine


class SwitchServo:
    def __init__(self, config):
        self.config = config
        self.ready = config.get('ready_angle')
        self.pressed = config.get('pressed_angle')
        self.not_ready = config.get('not_ready_angle')
        self.servo = machine.PWM(machine.Pin(config.get('servo_pin')), freq=50)
        self.current_angle = self.not_ready
        self.set_not_ready()

    async def _move_to_angle(self, angle, safety=True):
        old_angle = self.current_angle
        angle = max(0, min(180, angle))
        if safety:
            angle = max(angle, self.pressed)  # safety, never press too hard
        duty = int(26 + (angle / 180) * (128 - 26))
        self.servo.duty(duty)
        await asyncio.sleep(0.5 * abs(old_angle - angle) / 180)
        self.current_angle = angle
        self.servo.duty(0)

    async def click(self, return_movement=None):
        old_angle = self.current_angle
        await self._move_to_angle(self.pressed)
        await asyncio.sleep(self.config.get('click_length') / 1000.0)  # Convert ms to seconds
        if return_movement is None:
            await self._move_to_angle(old_angle)
        else:
            await return_movement()

    async def press(self):
        await self._move_to_angle(self.pressed)

    async def set_ready(self):
        await self._move_to_angle(self.ready)

    async def set_not_ready(self):
        await self._move_to_angle(self.not_ready)
