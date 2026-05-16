import dash_bootstrap_components as dbc
from components.generic.texts import Nome
from components.generic.elements import Divisor
from utils.functions import load_content, load_image
from dash import html, dcc


def indinvest_layout(lang='en'):
    txt = load_content("assets/contents/indinvest/texts.json", lang)
    
    return html.Div([
        
        html.Div([
            html.H1("Indipendent Investing", className="indinvest-title"),
        ], className="indinvest-tit"),
        
        html.Div([
            html.H1(txt['parOne']['title']),
            html.P(txt['parOne']['description'], className="ParOne-Indi"),

            html.Div([
                html.Div(html.P(txt['parTwo']['description']), className="LeftColumn-Indi"),
                html.Img(src="assets/contents/indinvest/par1.png", className="Img-Indi"),
            ], className="Content-Indi"),

            html.Div([
                html.Div(html.P(txt['parTre']['description']), className="LeftColumn-Indi"),
                html.Img(src="assets/contents/indinvest/par2.png", className="Img-Indi"),
            ], className="Content-Indi"),

            html.Div([
                html.Div(html.P(txt['parQua']['description']), className="LeftColumn-Indi"),
                html.Img(src="assets/contents/indinvest/par3.png", className="Img-Indi"),
            ], className="Content-Indi"),
            
        ], className="Cont-indi"),
        
        html.Div(" ", className="Dist-Indi")
    ])
