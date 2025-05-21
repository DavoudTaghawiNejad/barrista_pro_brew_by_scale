import yaml


def file_selector(argv):
    files_to_upload = read_files_to_upload()
    if '-a' in argv or '--all' in argv:
        files = []
        for f in files_to_upload.values():
            files += f
    elif len(argv) == 1:
        files = files_to_upload['wip']
    else:
        for arg in argv[1:]:
            if arg[0] != '-':
                if '.' in arg:
                    files += [arg]
                else:
                    files += files_to_upload[arg]

    return set(files)

def read_files_to_upload():
    with open("upload.yaml", "r") as f:
        data = yaml.safe_load(f)
    return data
