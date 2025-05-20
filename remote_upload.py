import sys
import urllib.request as urllib_request
import socket
from webrepl_cli import *
from davouds_esp_tools import file_selector


ESP32_IP = "coffee.local"  # Your ESP32 IP
REQUEST_PORT = "80"
WEBREPL_PORT = "8266"
PASSWORD = "12345678"          # Your WebREPL password
FILES_DIR = "."         # Directory with files


def send_file(file_name):
    s = socket.socket()
    ai = socket.getaddrinfo(ESP32_IP, WEBREPL_PORT)
    addr = ai[0][4]
    s.connect(addr)
    client_handshake(s)
    ws = websocket(s)
    login(ws, PASSWORD)
    ws.ioctl(9, 2)
    print(f'{file_name} - {ESP32_IP}:{WEBREPL_PORT}/{file_name}')
    put_file(ws, file_name, f'/{file_name}')
    s.close()


def post_request_esp32(endpoint):
    """Send a POST request to the specified endpoint on the ESP32."""
    try:
        request = f"http://{ESP32_IP}:{REQUEST_PORT}/{endpoint}"
        print(f'{request=}')
        # Prepare the request with POST method and empty JSON body
        req = urllib_request.Request(request, method='POST', data=b'{}')
        req.add_header('Content-Type', 'application/json')
        response = urllib_request.urlopen(req, timeout=5)
        if response.getcode() == 200:
            print(f"ESP32 {endpoint} successfully executed.")
        else:
            raise Exception(f"Failed to execute {endpoint} on ESP32. Status code: {response.getcode()}")
    except Exception as e:
        print(f"Error executing {endpoint} on ESP32: {e}")


if __name__ == '__main__':
    if '-w' in sys.argv or '--repl' in sys.argv or '--webrepl' in sys.argv:
        post_request_esp32('start_webrepl')
    elif '-r' in sys.argv or '--reset' in sys.argv:
        post_request_esp32('reset_esp32')
    else:
        files = file_selector(sys.argv)
        post_request_esp32('start_webrepl')
        print(f"Uploading to {ESP32_IP}...")
        for file_name in files:
            print(f"Uploading {file_name}...")
            send_file(file_name)
        print("Upload done.")
        post_request_esp32('reset_esp32')
        print("ESP32 resetted\nThe end!")
