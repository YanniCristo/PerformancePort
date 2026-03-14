import dash_bootstrap_components as dbc
from components.navbar import navbar
from components.cards import cards
from components.footer import footer
from components.paragraph import TitlePar
from components.login_modal import login_modal
from functions import load_content, load_image
import plotly.express as px
from dash import html, dcc


def indinvest_layout():
    txt = load_content("assets/contents/indinvest/texts.json")
    
    return html.Div([
        
        html.Div([
            html.H1("Indipendent Investing", className="indinvest-title"),
        ], className="indinvest-tit"),

        html.Div([
            html.H1(txt['parOne']['title'], className="indinvest-parOne-tit"),
            html.P(''.join(txt['parOne']['description']), className="indinvest-parOne-tit")
        ],
                 className="indinvest-parOne",
                 style={'padding': "60px 300px"}),

        TitlePar(txt['parTwo']['title'],
                 txt['parTwo']['description'],
                 "assets/contents/indinvest/par1.png",
                 txt['parTwo']['list'],
                 '3'),
        
        html.Div(style={"minHeight": "20vh"}),
        footer()

    ])
