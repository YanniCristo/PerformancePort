import dash_bootstrap_components as dbc
from components.navbar import navbar
from components.cards import cards
from components.login_modal import login_modal
from components.footer import footer
import plotly.express as px
from dash import html, dcc

def timehoriz_layout():
    
    return html.Div([
        
        html.Div([
            html.H1("Time Horizon", className="timehoriz-title"),
            ], className="timehoriz"),

        html.Div(style={"minHeight": "60vh"}),
        footer()
        
    ])
