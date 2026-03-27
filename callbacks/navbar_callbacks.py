from dash import Input, Output, State

def register(app):
    @app.callback(
        Output("navbar-collapse", "is_open"),
        Input("navbar-toggler", "n_clicks"),
        State("navbar-collapse", "is_open")
    )

    def toggle_navbar(n_clicks, is_open):
        if n_clicks:
            return not is_open
        return is_open
