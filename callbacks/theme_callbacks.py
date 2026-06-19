from dash import Input, Output, State

def register(app):
    @app.callback(
        Output("page-container", "className"),
        Output("theme-store", "data"),
        Input("settings-theme-toggle", "value"),  # ← value, non n_clicks
        prevent_initial_call=True
    )
    def switch_theme(is_dark):
        new_theme = "dark" if is_dark else "light"
        return new_theme, new_theme
