from dash import Input, Output, State

LANGS = ["us", "it", "en", "es", "fr", "de", "ru"]

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


    @app.callback(
        Output("lang-store", "data"),
        [Input(f"lang-{lang}", "n_clicks") for lang in LANGS],
        State("lang-store", "data"),
        prevent_initial_call=True
    )
    def update_lang(*args):
        from dash import ctx
        
        current_lang = args[-1]

        if ctx.triggered_id:
            return ctx.triggered_id.split("-")[1]

        return current_lang


    @app.callback(
        Output("lang-flag-active", "src"),
        Output("lang-label-active", "children"),
        Input("lang-store", "data")
    )
    def update_lang_label(lang):
        lang = lang or "us"
        return f"/assets/contents/flags/{lang}.svg", lang.upper()
