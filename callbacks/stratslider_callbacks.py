import dash
from dash import Input, Output, State, ALL, ctx
from utils.functions import load_content

CARDS_DICT = load_content('assets/contents/equitystrategy/Strategies.json')
CARDS = list(CARDS_DICT.values())
CARDS_KEYS = list(CARDS_DICT.keys())

CARD_WIDTH = 240
GAP = 12

def register(app):

    # Click sulle frecce → scorre le strategie
    @app.callback(
        Output("slider-index", "data"),
        Output("prev-btn", "disabled"),
        Output("next-btn", "disabled"),
        Input("prev-btn", "n_clicks"),
        Input("next-btn", "n_clicks"),
        State("slider-index", "data"),
        prevent_initial_call=True
    )
    def navigate(prev, next_, idx):
        ctx = dash.callback_context.triggered_id
        max_idx = len(CARDS) - 1
        if ctx == "prev-btn":
            idx = max(0, idx - 1)
        elif ctx == "next-btn":
            idx = min(max_idx, idx + 1)
        return idx, idx == 0, idx >= max_idx

    app.clientside_callback(
        """
        function(idx) {
            var STEP = 240 + 12;
            var track = document.getElementById('cards-track');
            if (track) {
                track.style.transform = 'translateX(-' + (idx * STEP) + 'px)';
            }
            return window.dash_clientside.no_update;
        }
        """,
        Output("slider-dummy", "data"),
        Input("slider-index", "data"),
        prevent_initial_call=True
    )


    # Click sulla card → aggiorna selected-strategy e classi CSS
    @app.callback(
        Output("selected-strategy", "data"),
        Output({"type": "strategy-card", "index": ALL}, "className"),
        Output("strat-description-content", "children"),
        Input({"type": "strategy-card", "index": ALL}, "n_clicks"),
        prevent_initial_call=True
    )
    def select_card(n_clicks_list):
        triggered = ctx.triggered_id
        if not triggered:
            raise dash.exceptions.PreventUpdate

        selected_key = triggered["index"]
        card_data = CARDS_DICT[selected_key]

        classes = [
            "slider-card selected-card" if k == selected_key else "slider-card"
            for k in CARDS_KEYS
        ]

        description = card_data.get("desc", "-")
        
        return selected_key, classes, description
