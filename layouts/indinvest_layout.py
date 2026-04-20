import dash_bootstrap_components as dbc
from components.navbar import navbar
from components.footer import footer
from components.generic.texts import Nome
from components.generic.elements import Divisor
from components.indinvest.paragraph import TitlePar
from utils.functions import load_content, load_image
from components.login_modal import login_modal
from dash import html, dcc


def indinvest_layout(lang='en'):
    txt = load_content("assets/contents/indinvest/texts.json", lang)
    
    return html.Div([
        
        html.Div([
            html.H1("Indipendent Investing", className="indinvest-title"),
        ], className="indinvest-tit"),
        
        html.Div([
            html.H1(txt['parOne']['title']),
            html.P(''.join(txt['parOne']['description'])),
            
            TitlePar(par=txt['parTwo']['description'],
                     img="assets/contents/indinvest/par1.png", num='01'),
            TitlePar(par=txt['parTre']['description'],
                     img="assets/contents/indinvest/par2.png", num='02'),
            TitlePar(par=txt['parQua']['description'],
                     img="assets/contents/indinvest/par3.png", num='03'),
            
        ], className="Cont-indi"),
        
        html.Div(" ", className="Dist-Indi"),
        footer()
    ])
