import dash_bootstrap_components as dbc
from components.navbar import navbar
from components.cards import cards
from components.login_modal import login_modal
import plotly.express as px
from dash import html, dcc

def strategies_layout():
    
    return html.Div([
        html.H1("Strategies page")
    ])
