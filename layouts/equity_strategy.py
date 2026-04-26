from utils.functions import load_content
from components.strat_slider import card_slider
from components.buttons import timeSelectbtn
import dash_bootstrap_components as dbc
from dash import html, dcc

from utils.data import data

def equity_strategy(lang='en'):

    accordion = dbc.Accordion([
        dbc.AccordionItem(
            title="Strategy description",
            children=[
                html.Div(id="strat-description-content"),
            ], item_id="strat-descript"
        )
    ], start_collapsed=True)

    dt_pkr = html.Div(
        dcc.DatePickerRange(
            id='date-picker',
            min_date_allowed=data.index.min(),
            max_date_allowed=data.index.max(),
            start_date=data.index.min(),
            end_date=data.index.max()
    ), className='picker-eqystr')
    

    return html.Div([

        html.H1("Equity Strategy", className="eqystr"),

        html.Div([

            # ---- SLIDER ----
            card_slider(),

            # ---- DESCRIPTION ----
            accordion,
            
            # ---- TOP PICKS + GRAFICO ----
            html.Div([

                # TOP PICKS
                html.Div([
                    html.H4("Selezione del mese"),

                    html.Div([
                        html.Span(" ")
                    ], className="selection-row"),
                    
                ], className="selection-box"),
        
                # GRAFICO
                html.Div([
                    html.Div([
                        dt_pkr,
                        timeSelectbtn(),
                    ], className='chart-toolbar'),

                    dcc.Graph(
                        id='graph',
                        config={'displayModeBar': False},
                        className='main-graph'
                        
                    )], className='Graph-container'),
                
            ], className='Graph-eqystr'),

            # ---- METRICHE ----
            html.Div(
                id="metrics-wrapper",
                className="metrics-wrapper"
            ),

        ], className='Cont-eqystr'),

        html.Div(" ", className="Dist-eqystr"),  
    ])
