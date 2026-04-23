from utils.functions import load_content
from components.generic.elements import Divisor
from components.buttons import timeSelectbtn
import dash_bootstrap_components as dbc
from dash import html, dcc

from utils.data import data

def equity_strategy(lang='en'):

    accordion = dbc.Accordion([
        dbc.AccordionItem(
            title="Description",
            children=[
                html.Div("Descrizione della strategia"),
                html.Div(""),
                html.Div(""),
            ],
            item_id="metrics"
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


    metrics_data = [
        ("Return", "12.5%"),
        ("Sharpe Ratio", "1.45"),
        ("Volatility", "8.2%"),
        ("Max Drawdown", "-6.3%"),
        ("Calmar Ratio", "1.98")]

    metric = html.Div(
        dbc.Row([
            dbc.Col(
                dbc.Card(
                    dbc.CardBody([
                        html.Div(name, className="metric-title"),
                        html.Div(value, className="metric-value"),
                    ])
                ),
                xs=12,
                sm=6,
                md=4,
                lg=3,
                xl=2
            )
            for name, value in metrics_data
        ], className="g-3 justify-content-center"),
        
        className="metrics-wrapper"
    )

    return html.Div([

        html.H1("Equity Strategy", className="eqystr"),

        html.Div([
            
            # ---- CONTROLLI ----
            html.Div([
                dcc.Dropdown(
                    id='ticker-dropdown',
                    options=[{'label': t, 'value': t} for t in data.columns],
                    value='S&P',
                    clearable=False
                ),
            ], className='control-eqystr'),

            accordion,
            
            # ---- METRICHE + GRAFICO (STESSO LIVELLO) ----
            html.Div([

                html.Div([
                    html.H4("Selezione del mese"),

                    html.Div([
                        html.Span("Return"),
                        html.Span("12.5%")
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

            metric,

        ], className='Cont-eqystr'),

        html.Div(" ", className="Dist-eqystr"),  
    ])
