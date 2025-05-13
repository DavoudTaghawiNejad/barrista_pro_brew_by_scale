#!/usr/bin/env python3

import subprocess
from remote_upload import py_files, html_files, json_files




MPREMOTE = "./.venv/bin/mpremote"
DEVICE = "/dev/tty.SLAB_USBtoUART"
SCREEN_SESSION = "espscreensession"
BAUD_RATE = "115200"

def upload_files():
    print("Uploading files to ESP32...")
    for file in py_files + html_files + json_files:
        print(f"Uploading {file}...")
        result = subprocess.run(
            [MPREMOTE, "connect", DEVICE, "fs", "cp", file, ":"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        if result.returncode != 0:
            print(f"Failed to upload {file}")
            print(result.stderr.decode())
            return False
    print("All files uploaded successfully.")
    return True

def quit_screen():
    subprocess.run(["screen", "-S", SCREEN_SESSION, "-X", "quit"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def open_screen():
    try:
        subprocess.run(
            ["screen", "-S", SCREEN_SESSION, DEVICE, BAUD_RATE],
            check=True
        )
        print("Exited screen normally.")
    except subprocess.CalledProcessError:
        print("Screen session failed. Restarting.")
        quit_screen()
        subprocess.run(["screen", "-S", SCREEN_SESSION, DEVICE, BAUD_RATE])

def main():
    try:
        print("Press ctrl+a, ctrl+d, y to exit screen session")
        while True:
            if not upload_files():
                quit_screen()
                upload_files()
            open_screen()
            print('ctrl-c for break, enter for upload')
            input()
    except Exception:
        quit_screen()


if __name__ == "__main__":
    main()
