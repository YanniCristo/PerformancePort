from components.login_modal import login_modal
import dash_bootstrap_components as dbc
from components.contact_form import contact_form
from components.navbar import navbar
from components.footer import footer
from dash import html, dcc
from utils.functions import load_content


def FAQ_layout():
    txt = load_content("assets/contents/contact/texts.json")
    descr = txt['info']['description']
    
    return html.Div([

        # NavBar
        navbar(),
        
        html.Div([
            html.H1("FAQ", className="hero-title"),
            ], className="FAQ"),
        
        html.Div([
            html.P(descr, className="cont-descr")
            ],
                 className="cust-care2",
                 style={"padding": "80px 200px",
                        "text-align": "center"}),

        html.Div(style={"minHeight": "30vh"}),
        footer(),
        login_modal()
        
        ])
