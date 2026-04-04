from components.signup_modal import signup_modal
from components.login_modal import login_modal
from components.navbar import navbar

import dash_bootstrap_components as dbc
from dash import html, dcc

def main_layout():
    return html.Div([
        dcc.Location(id="url", refresh=False),

        # Store per forzare refresh auth state dopo login
        dcc.Store(id="auth-event", data=0),
        
        navbar(),
        
        html.Div(id="page-content"),
        
        login_modal(),
        signup_modal()
    ])
