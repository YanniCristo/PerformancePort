import dash_bootstrap_components as dbc
from components.navbar import navbar
from components.cards import cards
from components.footer import footer
from components.login_modal import login_modal
import plotly.express as px
from functions import load_content
from dash import html, dcc
import pandas as pd

def home_layout():
    txt = load_content("contents/home/texts.json")
    title = txt['info']['title']
    descr = txt['info']['description']
    
    return html.Div([

        # hero
        html.Div([
            html.H1("Intelligent investments", className="hero-title"),
            html.P("Professional invetments insights", className="hero-subtitle"),
            dbc.Button("Start now", id="start-btn", color="primary", size="lg")
            ], className="hero"),

        html.Div([
            html.Img(
                    src="/assets/logo2.png",
                    style={"height": "35px"}
                    )
            ],
                 style={"padding-top": "55px",
                        "text-align": "center"}),

        html.Div([
            html.H1(title, className="descr-title"),
            html.P(descr, className="descr-descr")
            ], className="descr",
                 style={"padding": "100px 250px",
                        "text-align": "center"}),
        
        html.Div(style={"minHeight": "20vh"}),
        footer(),
        login_modal(),
        
        ])
