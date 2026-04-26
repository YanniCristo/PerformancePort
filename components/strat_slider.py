from utils.functions import load_content
from dash import html, dcc

CARDS_DICT = load_content('assets/contents/equitystrategy/Strategies.json')
CARDS = list(CARDS_DICT.values())
CARDS_KEYS = list(CARDS_DICT.keys())

def make_card(card, key, index, width="240px", selected=False):
    color = card.get('color', 'blue')
    classe = "slider-card selected-card" if selected else "slider-card"
    valcolor = "green"
    
    return html.Div([
        html.Span(card["tag"], className=f"card-tag tag-{color}"),
        html.P(card["title"], className="card-title"),
        html.P(card["freq"], className="card-desc"),
        html.Span(card["value"], className=f"card-value value-{valcolor}"),
    ],
        id={"type": "strategy-card", "index": key},   # id pattern-matching
        className=classe,
        style={"width": width, "cursor": "pointer"},
        n_clicks=0
    )

def card_slider(card_width=240):
    cards = CARDS

    return html.Div([
        dcc.Store(id="slider-index", data=0),
        dcc.Store(id="slider-dummy", data=0),   # output dummy per clientside callback
        dcc.Store(id="selected-strategy", data=CARDS_KEYS[0]),
        
        html.Div([
            html.Button("←", id="prev-btn", n_clicks=0, disabled=True, className="arrow-btn"),
            
            html.Div(
                html.Div(
                    [make_card(c, k, i, f"{card_width}px", selected=(i==0))
                     for i, (c, k) in enumerate(zip(cards, CARDS_KEYS))],
                    id="cards-track",
                    className="cards-track",
                ), className="slider-viewport",
            ),
            
            html.Button("→", id="next-btn", n_clicks=0, className="arrow-btn"),
            
        ], className="slider-wrapper", id="slider-wrapper")
    ])
