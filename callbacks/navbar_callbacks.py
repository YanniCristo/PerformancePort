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
        Input("lang-en", "n_clicks"),
        Input("lang-it", "n_clicks"),
        State("lang-store", "data"),
        prevent_initial_call=True
    )
    def update_lang(n_en, n_it, current_lang):
        from dash import ctx
        if ctx.triggered_id == "lang-en":
            return "en"
        elif ctx.triggered_id == "lang-it":
            return "it"
        return current_lang



    @app.callback(
        Output("lang-en", "className"),
        Output("lang-it", "className"),
        Input("lang-store", "data")
    )
    def update_lang_classes(lang):
        en_class = "lang-btn active-lang" if lang == "en" else "lang-btn"
        it_class = "lang-btn active-lang" if lang == "it" else "lang-btn"
        return en_class, it_class
