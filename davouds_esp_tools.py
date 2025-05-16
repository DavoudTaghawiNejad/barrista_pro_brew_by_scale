import sys
import yaml


def file_selector():
    files = read_files_to_upload()['standard_files']
    if len(sys.argv) >= 1:
        for arg in sys.argv[1:]:
            if arg[0] != '-':
                files += read_files_to_upload()[arg]
    return set(files)

def read_files_to_upload():
    with open("upload.yaml", "r") as f:
        data = yaml.safe_load(f)
    return data
