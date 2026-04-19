from dash import html
import dash_bootstrap_components as dbc
import components.dropdown as dd

def TitlePar(par="", img=None, lista=None, num=""):

    if num: num = html.P(num, className="Indi-Num")

    ele = ""
    if lista:
        ele = html.Ul([html.Li(item) for item in lista])

    return html.Div([
        
        html.Div([
            html.Div([
                num,
                html.P(par, className="Indi-Par")
            ], className="LeftColumn-Indi"),

            html.Img(src=img, className="Img-Indi")
            
        ], className="Content-Indi")
        
    ], className=f"Paragr-Indi")
                    
