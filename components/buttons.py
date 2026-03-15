import dash_bootstrap_components as dbc
from dash import html

def login():

    return dbc.Button(
        ["Start now", html.Span("→", className="cta-icon")],
        id="start-btn",
        className="cta-dg cta-dg-primary-white cta-dg-with-icon"
    )
