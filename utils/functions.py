from dash import html
import webbrowser
import json

def open_browser(port):
	webbrowser.open_new('http://localhost:{}'.format(port))

def load_content(path):
    with open(path) as f:
        return json.load(f)

def load_image(path):
        return html.Img(src=path)
