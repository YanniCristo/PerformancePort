from dash import Input, Output

def theme_callbacks(app):
    @app.callback(
        Output("page-container", "className"),
        Input("theme-button", "n_clicks"),
        prevent_initial_call=True
        )

    def switch_theme(n):
        if n % 2 == 1:
            return "dark"
        return "light"
