import dash_bootstrap_components as dbc
from components.navbar import navbar
from components.footer import footer
from components.generic.texts import Nome
from components.generic.elements import Divisor
from components.indinvest.paragraph import TitlePar
from utils.functions import load_content, load_image
from components.login_modal import login_modal
from dash import html, dcc


def indinvest_layout():
    txt = load_content("assets/contents/indinvest/texts.json")
    
    return html.Div([

        # NavBar
        navbar(),
        
        html.Div([
            html.H1("Indipendent Investing", className="indinvest-title"),
        ], className="indinvest-tit"),

        html.Div([
            html.H1(txt['parOne']['title'], className="indinvest-parOne-tit"),
            html.P(''.join(txt['parOne']['description']), className="indinvest-parOne-tit")
        ],
                 className="indinvest-parOne",
                 style={'padding': "60px 300px"}),
        
        html.Div([Nome()], style={"background-color":'#4e7bbbad'}),

        TitlePar(par = txt['parTwo']['description'],
                 img = "assets/contents/indinvest/par1.png",
                 lista = txt['parTwo']['list'], num='01'),

        Divisor(col='#4e7bbbad', h=40),

        TitlePar(par = txt['parTre']['description'],
                 img= "assets/contents/indinvest/par2.png", num='02'),

        Divisor(col='#4e7bbbad', h=40),

        TitlePar(par = txt['parQua']['description'],
                 img= "assets/contents/indinvest/par3.png", num='03'),

        html.Div(" ", className="Dist-Indi"),
        footer(),
        login_modal()

    ])
