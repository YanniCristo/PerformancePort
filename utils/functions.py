from dash import html
import json

def load_content(path):
    with open(path) as f:
        return json.load(f)

def load_image(path, name='images'):
        return html.Img(src=path, className=name)
