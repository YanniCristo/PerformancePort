import dash_bootstrap_components as dbc
from dash import html, dcc

def create_layout():
    return html.Div([
        dcc.Location(id="url", refresh=False),
        html.Div(id="page-content"),
    ])
