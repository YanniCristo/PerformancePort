from utils.constants import CAROUSEL_IMAGES
from dash import Input, Output, State, ctx, ALL
import json


def register(app):

    @app.callback(
        Output("carousel-image", "src"),
        Output("carousel-index", "data"),
        Output({"type": "carousel-dot", "index": ALL}, "className"),
        Input("carousel-interval", "n_intervals"),
        Input({"type": "carousel-dot", "index": ALL}, "n_clicks"),
        State("carousel-index", "data"),
    )
    def update_carousel(n_intervals, dot_clicks, current_index):
        n = len(CAROUSEL_IMAGES)
        triggered = ctx.triggered_id

        if triggered == "carousel-interval":
            new_index = (current_index + 1) % n
        elif isinstance(triggered, dict) and triggered.get("type") == "carousel-dot":
            new_index = triggered["index"]
        else:
            new_index = current_index

        dot_classes = [
            "carousel-dot carousel-dot-active" if i == new_index else "carousel-dot"
            for i in range(n)
        ]

        return CAROUSEL_IMAGES[new_index], new_index, dot_classes
