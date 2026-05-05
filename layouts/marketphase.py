from utils.functions import load_content, load_image
import dash_bootstrap_components as dbc
from components.generic.elements import Divisor
from dash import html, dcc

def marketphase(lang='en'):
    txt = load_content("assets/contents/marketphase/texts.json", lang)
    path_img = "assets/contents/marketphase/"
    
    return html.Div([

        # Title
        html.H1("Market Phase", className="mktphse-title"),

        # Contents
        html.Div([

            html.H1(txt['parOne']['title'], className='title-mktphse'),
            html.P(txt['parOne']['descr'], className='par-mktphse'),
            load_image(f"{path_img}EquityTab.png", 'tab-mktphse'),
            load_image(f"{path_img}EquityChart.png", 'fig-mktphse'),
            Divisor(col='#4e7bbbad', h=30),
            
            html.H1(txt['parTwo']['title'], className='title-mktphse'),
            html.P(txt['parTwo']['descr'], className='par-mktphse'),
            load_image(f"{path_img}BondTab.png", 'tab-mktphse'),
            load_image(f"{path_img}BondChart.png", 'fig-mktphse'),

            ], className="Cont-mktphse"),

        # Bottom
        html.Div(" ", className="Dist-mktphse")
        
    ])
