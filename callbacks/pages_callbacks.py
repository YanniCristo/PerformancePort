from dash import Input, Output
from layouts.home_layout import home_layout
from layouts.market_layout import market_layout
from layouts.strategies_layout import strategies_layout
from layouts.results_layout import results_layout
from layouts.contact_layout import contact_layout

def register_callbacks(app):
    @app.callback(
        Output("page-content", "children"),
        Input("url", "pathname")
    )
    def display_page(pathname):

        if pathname == "/market":
            return market_layout()

        elif pathname == "/strategies":
            return strategies_layout()

        elif pathname == "/results":
            return results_layout()

        elif pathname == "/contact":
            return contact_layout()

        else:
            return home_layout()
