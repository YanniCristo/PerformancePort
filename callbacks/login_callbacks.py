from dash import Input, Output, State

def login_callbacks(app):

    @app.callback(
            Output("login-modal", "is_open"),
            Input("start-btn", "n_clicks"),
            State("login-modal", "is_open"),
            prevent_initial_call=True
    )
    def toggle_modal(n, is_open):
            return not is_open
