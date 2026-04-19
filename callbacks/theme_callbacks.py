from dash import Input, Output, State, callback_context

def register(app):
    @app.callback(
        Output("page-container", "className"),
        Output("theme-store", "data"),
        Input("theme-button", "n_clicks"),
        State("theme-store", "data"),
        prevent_initial_call=True
    )
    def switch_theme(n_clicks, current_theme):
        new_theme = "light" if current_theme == "dark" else "dark"
        return new_theme, new_theme
