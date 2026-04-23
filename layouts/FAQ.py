import dash_bootstrap_components as dbc
from components.contact_form import contact_form
from dash import html, dcc
from utils.functions import load_content


def FAQ_layout(lang='en'):
    txt = load_content("assets/contents/FAQ/texts.json", lang)
    descr = txt['parOne']['descr']
    
    return html.Div([
        
        html.H1("", className="FAQ-title"),
        
        html.Div([
            html.P(descr, className="cont-descr")
            ],
                 className="cust-care2",
                 style={"padding": "80px 200px",
                        "text-align": "center"}),

        html.Div(style={"minHeight": "30vh"})
        ])
