from components.login_modal import login_modal
import dash_bootstrap_components as dbc
from components.navbar import navbar
from components.footer import footer
from dash import html, dcc

def timehoriz_layout():
    
    return html.Div([

        # NavBar
        navbar(),
        
        html.Div([
            html.H1("Time Horizon", className="timehoriz-title"),
            ], className="timehoriz"),

        html.Div(style={"minHeight": "60vh"}),
        footer(),
        login_modal()
        
    ])
