from dash import html

def Nome():
    
    return html.H1([
        html.Span("P", className="texts-one"),
        html.Span("erforming", className="texts-two"),
        html.Span("P", className="texts-one"),
        html.Span("ort", className="texts-two"),
        ], className="MainNome")

def Divisor(col='#4e7bbbad', h=10):
    return html.Div([
        html.Div(className="Divisor-Indi")],
                    style={"background-color": col,
                           "height": f"{h}px"})
