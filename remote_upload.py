import os
import subprocess
import glob

ESP32_IP = "192.168.0.19"  # Your ESP32 IP
PASSWORD = "12341234"          # Your WebREPL password
FILES_DIR = "."         # Directory with files

print(f"Uploading to {ESP32_IP}...")
for suffix in ['py', 'html', 'json']:
    for file_path in glob.glob(f"*.{suffix}"):
        print(f"Uploading {file_path}...")
        subprocess.run([
            "python", "webrepl_cli.py", "-p", PASSWORD,
            file_path, f"{ESP32_IP}:/{os.path.basename(file_path)}"
        ])
print("Done.")
