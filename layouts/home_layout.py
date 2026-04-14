import dash_bootstrap_components as dbc
from components.navbar import navbar
from components.cards import cards_home
from components.footer import footer
from components.login_modal import login_modal
from utils.constants import CAROUSEL_IMAGES
from utils.functions import load_content
from dash import html, dcc

def home_layout():
    txt = load_content("assets/contents/home/texts.json")
    title = txt['info']['title']
    descr = txt['info']['description']
    
    return html.Div([

            # Carosello immagini
            html.Div([
                # Immagine corrente
                html.Img(
                    id="carousel-image",
                    src=CAROUSEL_IMAGES[0]
                ),
                # Pallini di navigazione
                html.Div([
                    html.Span(
                        id={"type": "carousel-dot", "index": i},
                        n_clicks=0,
                        className="carousel-dot" + (" carousel-dot-active" if i == 0 else ""),
                    )
                    for i in range(len(CAROUSEL_IMAGES))
                ], className="carousel-dots"),

                # Timer automatico
                dcc.Interval(id="carousel-interval", interval=6000, n_intervals=0),

                # Store per indice corrente
                dcc.Store(id="carousel-index", data=0),
            ], style={"margin-top": "25px",
                      "padding-top": "55px",
                      "text-align": "center", "position": "relative"}),


  
        html.Div([
            html.Img(
                    src="/assets/contents/general/logo2.png",
                    style={"height": "45px"}
                    )
            ],
                 style={"padding-top": "55px",
                        "text-align": "Center"}),

        html.Div([
            html.H1(title, className="descr-title"),
            html.P(descr, className="descr-descr")
            ], className="descr",
                 style={"padding": "100px 250px",
                        "text-align": "center"}),
            
        cards_home(),
        html.Div(style={"minHeight": "20vh"}),
        footer(),
        ])
