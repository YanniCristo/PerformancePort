from utils.functions import load_content, load_image
from components.ecoview.slider import card_slider
from components.buttons import timeSelectbtn
import dash_bootstrap_components as dbc
from dash import html, dcc

from utils.macrodata import macro

def eco_view(lang='en'):

    return html.Div([

        html.H1("Economic Overview", className="title-ecoview"),
        
        html.Div([
            
            # SliderCards per selezionare trimestre
            card_slider(lang=lang),
            
            html.Div(id='artic-ecoview')
            
                 ], className="main-ecoview"),
        
        html.Div(" ", className="Dist-ecoview")
    ])
