from components.login_modal import login_modal
from utils.functions import load_content, load_image
from components.generic.elements import Divisor
from components.buttons import timeSelectbtn
import dash_bootstrap_components as dbc
from components.navbar import navbar
from components.footer import footer
from dash import html, dcc

from utils.data import data

def equity_strategy():

    return html.Div([

        # NavBar
        navbar(),

        html.H1("Equity Strategy", className="eqystr"),

        html.Div([
            
            html.Div([
                
                # Date Picker
                html.Div(
                    dcc.DatePickerRange(id='date-picker',
                                        min_date_allowed=data.index.min(),
                                        max_date_allowed=data.index.max(),
                                        start_date=data.index.min(),
                                        end_date=data.index.max()
                                        ), className='picker-div'),
            
                # Dropdown per selezionare ticker
                dcc.Dropdown(id='ticker-dropdown',
                             options=[{'label': t, 'value': t} for t in data.columns],
                             value='S&P',
                             clearable=False
                             ),
                ], className='control-eqystr'),
            
            # Grafico
            html.Div([
                timeSelectbtn(),
                dcc.Graph(id='graph',
                          config={'displayModeBar': False},
                          className='main-graph'),
                ], className='Graph-eqystr'),
            
            ], className='Cont-eqystr'),
        
        html.Div(" ", className="Dist-eqystr"),
        footer(),
        login_modal()
        
    ])
