import dash_bootstrap_components as dbc
from components.cards import cards
import plotly.express as px
from dash import html, dcc
import pandas as pd

df = pd.DataFrame({
    "Month": ["Gen", "Feb", "Mar", "Apr"],
    "Return": [100, 120, 90, 140]})
fig = px.line(df, x="Month", y="Return")

def model_layout():
    
    return html.Div([
        cards(),
        dbc.Container([
            dcc.Graph(figure=fig)
        ], className="mt-4")
        
    ])
