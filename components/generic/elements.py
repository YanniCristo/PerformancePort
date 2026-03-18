from dash import html

def Divisor(col='#4e7bbbad', h=10):
    return html.Div([
        html.Div(className="Divisor")],
                    style={"margin-top": f"{h}px",
                           "margin-bottom": f"{h}px"})
