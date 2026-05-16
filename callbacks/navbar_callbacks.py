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



    @app.callback(
        Output("lang-store", "data"),
        Input("lang-us", "n_clicks"),
        Input("lang-it", "n_clicks"),
        Input("lang-en", "n_clicks"),
        Input("lang-es", "n_clicks"),
        Input("lang-fr", "n_clicks"),
        Input("lang-de", "n_clicks"),
        Input("lang-ru", "n_clicks"),
        State("lang-store", "data"),
        prevent_initial_call=True
    )
    def update_lang(n_us, n_it, n_en, n_es, n_fr, n_de, n_ru,
                    current_lang):
        from dash import ctx
        if ctx.triggered_id == "lang-us":
            return "us"
        elif ctx.triggered_id == "lang-it":
            return "it"
        elif ctx.triggered_id == "lang-en":
            return "en"
        elif ctx.triggered_id == "lang-es":
            return "es"
        elif ctx.triggered_id == "lang-fr":
            return "fr"
        elif ctx.triggered_id == "lang-de":
            return "de"
        elif ctx.triggered_id == "lang-ru":
            return "ru"
        return current_lang



    @app.callback(
        Output("lang-flag-active", "src"),
        Output("lang-label-active", "children"),
        Input("lang-store", "data")
    )
    def update_lang_label(lang):
        lang = lang or "us"
        return f"/assets/contents/flags/{lang}.svg", lang.upper()
