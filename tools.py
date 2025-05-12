def load_html_generatory(file):
    with open(file) as f:
        while True:
            chunk = f.read(1024)
            if not chunk:
                break
            yield chunk
