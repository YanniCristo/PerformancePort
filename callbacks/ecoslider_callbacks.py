import dash
from dash import Input, Output, State, ALL, ctx
from utils.macrodata import macro

QUARTERS = sorted(macro, reverse=True)
CARD_WIDTH = 240
GAP = 12

def register(app):

    ############################################################################
    # ── Frecce: aggiorna indice e stato disabled ──────────────────────────────
    @app.callback(
        Output("eco-slider-index", "data"),
        Output("eco-prev-btn", "disabled"),
        Output("eco-next-btn", "disabled"),
        Input("eco-prev-btn", "n_clicks"),
        Input("eco-next-btn", "n_clicks"),
        State("eco-slider-index", "data"),
        prevent_initial_call=True
    )
    def navigate_quarters(prev, next_, idx):
        triggered = dash.callback_context.triggered_id
        max_idx = len(QUARTERS) - 1
        if triggered == "eco-prev-btn":
            idx = max(0, idx - 1)
        elif triggered == "eco-next-btn":
            idx = min(max_idx, idx + 1)
        return idx, idx == 0, idx >= max_idx

    # ── Clientside: sposta il track CSS ──────────────────────────────────────
    app.clientside_callback(
        """
        function(idx) {
            var STEP = 240 + 12;
            var track = document.getElementById('eco-cards-track');
            if (track) {
                track.style.transform = 'translateX(-' + (idx * STEP) + 'px)';
            }
            return window.dash_clientside.no_update;
        }
        """,
        Output("eco-slider-dummy", "data"),
        Input("eco-slider-index", "data"),
        prevent_initial_call=True
    )    

    ############################################################################
    # Click sulla card → aggiorna selected-q e classi CSS
    @app.callback(
        Output("selected-q", "data"),
        Output({"type": "quarter-card", "index": ALL}, "className"),
        Input({"type": "quarter-card", "index": ALL}, "n_clicks"),
        prevent_initial_call=True
    )
    def select_quarter(n_clicks_list):
        triggered = ctx.triggered_id
        if not triggered:
            raise dash.exceptions.PreventUpdate

        selected_q = triggered["index"]

        classes = [
            "slider-q selected-q" if q == selected_q else "slider-q"
            for q in QUARTERS
        ]

        return selected_q, classes
