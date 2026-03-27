from datetime import datetime
from dash import html
import webbrowser
import json

def open_browser(port):
	webbrowser.open_new('http://localhost:{}'.format(port))

def load_content(path):
    with open(path) as f:
        return json.load(f)

def load_image(path, name='images'):
        return html.Img(src=path, className=name)

def q_to_dt(q_str: str) -> datetime:
    year_str, quarter_str = q_str.split('-Q')
    year = int(year_str)
    quarter = int(quarter_str)

    quarter_end = {
        1: (3, 31), 2: (6, 30),
        3: (9, 30), 4: (12, 31)}

    month, day = quarter_end[quarter]
    return datetime(year, month, day)

