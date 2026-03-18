from components.login_modal import login_modal
from utils.functions import load_content, load_image
from components.generic.elements import Divisor
import dash_bootstrap_components as dbc
from components.navbar import navbar
from components.footer import footer
from dash import html, dcc

def timehoriz_layout():
    txt = load_content("assets/contents/timehoriz/texts.json")
    path_img = "assets/contents/timehoriz/"
    
    return html.Div([

        # NavBar
        navbar(),
        
        html.Div([
            html.H1("Time Horizon", className="timehoriz-title"),
            ], className="timehoriz"),

        html.Div([

            html.P(txt['parOne']['descr'], className='par-time'),
            load_image(f"{path_img}fig1.png", 'fig-time'),
            Divisor(col='#4e7bbbad', h=30),

            html.H1(txt['parTwo']['title'], className='tit-time'),
            html.P(txt['parTwo']['descr'], className='par-time'),
            load_image(f"{path_img}fig2.png", 'fig-time'),
            load_image(f"{path_img}tab1.png", 'tab-time'),
            Divisor(col='#4e7bbbad', h=30),

            html.H1(txt['parTre']['title'], className='tit-time'),
            html.P(txt['parTre']['descr'], className='par-time'),
            load_image(f"{path_img}fig3.png", 'fig-time'),
            load_image(f"{path_img}tab2.png", 'tab-time'),
            
            ], className="Cont-Time"),
        

        html.Div(" ", className="Dist-Time"),
        footer(),
        login_modal()
        
    ])
