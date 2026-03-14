from dash import html
import dash_bootstrap_components as dbc
import components.dropdown as dd

def TitlePar(tit,par,img,lista=None,name=""):
    if lista:
        ele = html.Ul([
            html.Li(item) for item in lista
            ])
    else:
        ele=""

    return html.Div([

        html.H2(tit, className="TitlePar-tit"),

        html.Div([
            html.P(par, className="TitlePar-par"),
            ele,
            html.Img(src=img, className="TitlePar-img")
        ],
        className="TitlePar-content")

    ],
    className=f"TitlePar-{name}",
    style={'padding': "60px 300px"})
