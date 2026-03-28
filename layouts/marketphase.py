from components.login_modal import login_modal
from utils.functions import load_content, load_image
import dash_bootstrap_components as dbc
from components.generic.elements import Divisor
from components.navbar import navbar
from components.footer import footer
from dash import html, dcc

def marketphase():
    txt = load_content("assets/contents/marketphase/texts.json")
    path_img = "assets/contents/marketphase/"
    
    return html.Div([

        # NavBar
        navbar(),
        
        html.Div(
            html.H1("Market Phase", className="marketphase-title")
            ),

        footer(),
        login_modal()
        
    ])
