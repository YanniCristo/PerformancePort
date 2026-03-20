from components.login_modal import login_modal
from utils.functions import load_content, load_image
import dash_bootstrap_components as dbc
from components.generic.elements import Divisor
from components.navbar import navbar
from components.footer import footer
from dash import html, dcc

def market_layout():
    txt = load_content("assets/contents/market/texts.json")
    path_img = "assets/contents/market/"
    
    return html.Div([

        # NavBar
        navbar(),
        
        html.Div([
            html.H1("Market Cycle", className="market-title"),
            ], className="market"),

        html.Div([
            
            html.H1(txt['parOne']['title'], className='tit-mkt'),
            html.P(txt['parOne']['descr'], className='par-mkt'),
            load_image(f"{path_img}tab1.png", 'tab-mkt'),
            Divisor(col='#4e7bbbad', h=30),

            html.H1(txt['parTwo']['title'], className='tit-mkt'),
            html.P(txt['parTwo']['descr'], className='par-mkt'),
            load_image(f"{path_img}fig1.png", 'fig-mkt'),
            Divisor(col='#4e7bbbad', h=30),

            html.H1(txt['parTre']['title'], className='tit-mkt'),
            html.P(txt['parTre']['descr'], className='par-mkt'),
            load_image(f"{path_img}fig2.png", 'fig-mkt'),
            Divisor(col='#4e7bbbad', h=30),

            html.H1(txt['parFou']['title'], className='tit-mkt'),
            html.P(txt['parFou']['descr'], className='par-mkt'),
            Divisor(col='#4e7bbbad', h=30),

            html.H1(txt['parFiv']['title'], className='tit-mkt'),
            html.P(txt['parFiv']['descr'], className='par-mkt'),
            load_image(f"{path_img}fig3.png", 'fig-mkt'),
            Divisor(col='#4e7bbbad', h=30),

            html.H1(txt['parSix']['title'], className='tit-mkt'),
            html.P(txt['parSix']['descr'], className='par-mkt'),
            load_image(f"{path_img}fig4.png", 'fig-mkt'),

            ], className="Cont-mkt"),

        html.Div(" ", className="Dist-mkt"),
        footer(),
        login_modal()
        
    ])
