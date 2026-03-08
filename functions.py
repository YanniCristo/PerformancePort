import json

def load_content(path):
    with open(path) as f:
        return json.load(f)
