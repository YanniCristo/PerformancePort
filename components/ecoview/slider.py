from utils.macrodata import macro
from dash import html, dcc

def make_card(q, index, width="240px", selected=False):
    classe = "slider-q selected-q" if selected else "slider-q"
    
    return html.Div([
        html.Span(q, className=f"q-tag")
    ], id={"type": "quarter-card", "index": q},   # id pattern-matching
        className=classe,
        style={"width": width, "cursor": "pointer"},
        n_clicks=0
    )

def card_slider(card_width=240, lang='en'):
    quarters = sorted(macro, reverse=True)
    default_q = quarters[0]
    
    return html.Div([
        dcc.Store(id="eco-slider-index", data=0),
        dcc.Store(id="eco-slider-dummy", data=0),   # output dummy per clientside callback
        dcc.Store(id="selected-q", data=default_q),
        
        html.Div([
            html.Button("←", id="eco-prev-btn", n_clicks=0, disabled=True, className="arrow-btn"),
            
            html.Div(
                html.Div(
                    [make_card(q, i, f"{card_width}px", selected=(q == default_q))
                     for i, q in enumerate(quarters)],
                    id="eco-cards-track",
                    className="cards-track",
                ), className="slider-viewport",
            ),
            
            html.Button("→", id="eco-next-btn", n_clicks=0, className="arrow-btn"),
            
        ], className="slider-wrapper", id="eco-slider-wrapper")
    ])
