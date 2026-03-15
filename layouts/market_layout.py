from components.login_modal import login_modal
from utils.functions import load_content
import dash_bootstrap_components as dbc
from components.navbar import navbar
from components.footer import footer
from dash import html, dcc

def market_layout():
    
    return html.Div([

        # NavBar
        navbar(),
        
        html.Div([
            html.H1("Market Cycle", className="market-title"),
            ], className="market"),

        html.Div(style={"minHeight": "60vh"}),
        footer(),
        login_modal()
        
    ])
