import dash_bootstrap_components as dbc
from dash import html

def login():

    return dbc.Button(
        ["Start now", html.Span("→", className="cta-icon")],
        id="start-btn",
        className="cta-dg cta-dg-primary-white cta-dg-with-icon"
    )

def timeSelectbtn():

    return html.Div([
        dbc.Button('1Y', id="1Y-btn"),
        dbc.Button('3Y', id="3Y-btn"),
        dbc.Button('5Y', id="5Y-btn"),
        dbc.Button('Max', id="Max-btn")
        ], className='Chart-btn')
