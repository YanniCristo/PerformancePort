import dash_bootstrap_components as dbc
from dash import html

def timeSelectbtn():

    return html.Div([
        dbc.Button('1Y', id="1Y-btn"),
        dbc.Button('3Y', id="3Y-btn"),
        dbc.Button('5Y', id="5Y-btn"),
        dbc.Button('Max', id="Max-btn")
        ], className='Chart-btn')
