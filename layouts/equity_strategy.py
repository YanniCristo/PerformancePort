from utils.functions import load_content
from components.strat_slider import card_slider

from components.locked_section import locked_section
from components.buttons import timeSelectbtn
import dash_bootstrap_components as dbc
from dash import html, dcc
from utils.data import data
from utils.text_parser import parse_rich_text

def equity_strategy(lang='en'):
    intest = load_content(f"assets/contents/equitystrategy/Info.json", lang)['INTEST']
    discla = load_content(f"assets/contents/equitystrategy/Info.json", lang)['DISCLAMER']

    strategies = load_content('assets/contents/equitystrategy/Strategies.json', lang=lang)
    first_key = list(strategies.keys())[0]
    default_description = strategies[first_key].get("desc", "")
        
    accordion = dbc.Accordion([
        dbc.AccordionItem(
            title=intest['descr'],
            children=[
                html.Div(default_description, id="strat-description-content"),
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

    # Store per l'indice della composizione visualizzata (0 = più recente)
    holdings_store = dcc.Store(id="holdings-date-index", data=0)

    # Intestazione selection-box con titolo e frecce di navigazione
    selection_header = html.Div([
        html.H4(intest['topMO'], className="selection-box-title"),
        html.Div([
            html.Button("←", id="holdings-prev-btn", className="holdings-nav-btn", n_clicks=0),
            html.Span(id="holdings-date-label", className="holdings-date-label"),
            html.Button("→", id="holdings-next-btn", className="holdings-nav-btn", n_clicks=0),
        ], className="holdings-nav-controls"),
    ], className="selection-box-header")

    disclamer = html.Div(parse_rich_text(discla), className="eqy-disclamer")
    

    return html.Div([

        html.H1("Equity Strategy", className="eqystr"),
        holdings_store,

        html.Div([

            # ---- SLIDER ----
            card_slider(lang=lang),

            # ---- DESCRIPTION ----
            accordion,
            
            # ---- TOP PICKS + GRAFICO ----
            html.Div([

                # TOP PICKS
                locked_section(
                    content=html.Div([
                        selection_header,
                        html.Div(id="selection-row", className="selection-row"),
                    ], className="selection-box"),
                    required_tier="pro",
                    section_id="top-picks-lock"
                ),
                
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
        disclamer,
    ])
