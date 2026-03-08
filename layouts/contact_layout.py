import dash_bootstrap_components as dbc
from components.contact_form import contact_form
from dash import html, dcc
from functions import load_content


def contact_layout():
    txt = load_content("contents/contact/texts.json")
    descr = txt['info']['description']
    
    return html.Div([
        
        html.Div([
            html.H1("Customer care", className="hero-title"),
            ], className="cust-care1"),

        html.Div([
            html.Img(
                    src="/assets/logo2.png",
                    style={"height": "35px"}
                    )
            ],
                 style={"padding-top": "55px",
                        "text-align": "center"}),
        
        html.Div([
            html.P(descr, className="cont-descr")
            ],
                 className="cust-care2",
                 style={"padding": "80px 200px",
                        "text-align": "center"}),
        html.Div([
            contact_form(),
            html.Div(style={"minHeight": "20vh"})
            ],  style={"padding": "0px 520px"})
        
        ])
