from components.signup_modal import signup_modal
from components.login_modal import login_modal
from components.settings_modal import settings_modal
from components.navbar import navbar
from components.footer import footer

import dash_bootstrap_components as dbc
from dash import html, dcc

def main_layout():
    return html.Div(
        id="page-container",
        className="light",
        
        children=[
            dcc.Location(id="url", refresh=False),

            # Store lingua: 'en' - persiste durante la sessione
            dcc.Store(id="lang-store", data="en", storage_type="local"),

            # Store per forzare refresh auth state dopo login
            dcc.Store(id="auth-event", data=0),

            # Store per tipo di utente (anonymous|registered|pro)
            dcc.Store(id="user-tier", data="anonymous"),

            # Redirect pagamenti Stripe
            dcc.Location(id="redirect", refresh=True),

            # Store per il checkout Stripe
            dcc.Store(id="checkout-session", data={}),

            # Store per il trigger del menù settings
            dcc.Store(id="settings-trigger", data=0),

            # Store per lo stile del sito
            dcc.Store(id="theme-store", data="light"),
            
            navbar(),
            html.Div(id="page-content"),
            footer(),

            # Modals
            login_modal(),
            settings_modal(),
            signup_modal(),
        ]
    )
