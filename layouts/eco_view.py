from components.login_modal import login_modal
from utils.functions import load_content, load_image
from components.generic.elements import Divisor
from components.buttons import timeSelectbtn
import dash_bootstrap_components as dbc
from components.navbar import navbar
from components.footer import footer
from dash import html, dcc

from utils.macrodata import macro

def eco_view():

    return html.Div([

        html.H1("Economic Overview", className="title-ecoview"),
        
        html.Div([
            
            # Dropdown per selezionare ticker
            dcc.Dropdown(id='quarter-dd',
                         options=[{'label': t, 'value': t} for t in macro],
                         value=macro[0],
                         clearable=False,
                         className='quarter-dd'),
            
            html.Div(id='artic-ecoview')
            
                 ], className="main-ecoview"),
        
        html.Div(" ", className="Dist-ecoview"),
        footer()
    ])
