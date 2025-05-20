import yaml


def file_selector(argv):
    files_to_upload = read_files_to_upload()
    if '-a' in argv or '--all' in argv:
        print(files_to_upload)
        files = []
        for f in files_to_upload.values():
            files += f
    else:
        files = files_to_upload['wip']

    if len(argv) >= 1:
        for arg in argv[1:]:
            if arg[0] != '-':
                files += files_to_upload[arg]
    return set(files)

def read_files_to_upload():
    with open("upload.yaml", "r") as f:
        data = yaml.safe_load(f)
    return data
