import asyncio
import network  # type: ignore


class Wifi:
    def __init__(self, ssid, password):
        self.ssid = ssid
        self.password = password
        self.wlan = network.WLAN(network.STA_IF)
        self.wlan.active(True)
        self.wlan.connect(ssid, password)
        self.wlan.config(hostname='coffee')

    async def display_credentials_until_connected(self, display):
        time = 0
        while not self.wlan.isconnected():
            if time > 120:  # 120 -> 30 seconds
                await display.show_text_timed(f'No connection:\nSSID:\n{self.ssid}\nPassword:\n{self.password}', inverted=True)
            time += 1
            await asyncio.sleep(0.25)
        print("Wi-Fi connected. IP:", self.wlan.ifconfig()[0])
        print('coffee.local')
