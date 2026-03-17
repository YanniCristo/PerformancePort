from dash import html

def Divisor(col='#4e7bbbad', h=10):
    return html.Div([
        html.Div(className="Divisor-Indi")],
                    style={"background-color": col,
                           "height": f"{h}px"})
