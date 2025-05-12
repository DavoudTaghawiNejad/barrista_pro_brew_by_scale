import os
import subprocess

ESP32_IP = "192.168.0.19"  # Your ESP32 IP
PASSWORD = "12341234"          # Your WebREPL password
FILES_DIR = "."         # Directory with files

py_files = [
'boot.py',
'coffee_machine.py',
'coffee_storage.py',
'display.py',
'fake_coffee_machine.py',
'hx711.py',
'main.py',
'microdot.py',
'network_tools.py',
'pcd8544.py',
'scale.py',
'storage.py',
'switch_servo.py',
'tools.py']

html_files = ['config.html', 'webpage.html']

json_files = ['config.json']

print(f"Uploading to {ESP32_IP}...")
for suffix in ['py', 'html', 'json']:
    for file_path in py_files + html_files + json_files:
        print(f"Uploading {file_path}...")
        subprocess.run([
            "python", "webrepl_cli.py", "-p", PASSWORD,
            file_path, f"{ESP32_IP}:/{os.path.basename(file_path)}"
        ])
print("Done.")
