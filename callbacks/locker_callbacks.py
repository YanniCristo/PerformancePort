from dash import Output, Input

def register(app):

    @app.callback(
        Output("top-picks-lock", "style"),           # overlay
        Output("top-picks-lock-content", "style"),   # contenuto
        Input("user-tier", "data")
    )
    def toggle_top_picks_lock(tier):
        if tier == "pro":
            return (
                {"display": "none"},                          # overlay nascosto
                {"filter": "none", "pointerEvents": "auto"}  # contenuto nitido
            )
        return (
            {"display": "flex"},                                       # overlay visibile
            {"filter": "blur(4px)", "pointerEvents": "none"}          # contenuto sfumato
        )
