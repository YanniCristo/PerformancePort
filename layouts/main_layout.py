import dash_bootstrap_components as dbc
from components.navbar import navbar
from components.cards import cards
from components.login_modal import login_modal
import plotly.express as px
from dash import html, dcc
import pandas as pd

df = pd.DataFrame({
    "mese": ["Gen", "Feb", "Mar", "Apr"],
    "vendite": [100, 120, 90, 140]})
fig = px.line(df, x="mese", y="vendite")

def create_layout():
    return html.Div([
        navbar(),
        dcc.Location(id="url", refresh=False),
        html.Div(id="page-content"),
    ])
