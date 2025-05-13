import asyncio
import network


def connect_wifi(ssid, password):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print("Connecting to Wi-Fi...")
        wlan.connect(ssid, password)
    if wlan.isconnected():
        print("Wi-Fi connected. IP:", wlan.ifconfig()[0])


async def wifi_credentials_until_wifi_is_on(ssid, password, display):
    wlan = network.WLAN(network.STA_IF)
    time = 0
    while not wlan.isconnected():
        if time > 120:  # 120 -> 30 seconds
            await display.show_text_timed(f'SSID:\n{ssid}\nPassword:\n{password}', inverted=True)
        time += 1

        await asyncio.sleep(0.25)
    print("Wi-Fi connected. IP:", wlan.ifconfig()[0])
