from components.login_modal import login_modal
from utils.functions import load_content, load_image
import dash_bootstrap_components as dbc
from components.generic.elements import Divisor
from components.navbar import navbar
from components.footer import footer
from dash import html, dcc

def macroallocation():
    txt = load_content("assets/contents/macroallocation/texts.json")
    path_img = "assets/contents/macroallocation/"
    
    return html.Div([

        # Title
        html.H1("Portfolio Construction", className="macroall-title"),

        # Contents
        html.Div([

            html.P(txt['parOne']['descr'], className='par-macroall'),
            load_image(f"{path_img}Ron.png", 'tab-macroall'),
            Divisor(col='#4e7bbbad', h=30),
            load_image(f"{path_img}Ronoff.png", 'tab-macroall'),
            Divisor(col='#4e7bbbad', h=30),
            load_image(f"{path_img}Roff.png", 'tab-macroall')

            ], className="Cont-macroall"),

        # Bottom
        html.Div(" ", className="Dist-macroall"),
        footer()
    ])
