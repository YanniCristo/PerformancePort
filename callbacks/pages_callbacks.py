from dash import Input, Output
from layouts.home_layout import home_layout
from layouts.indinvest_layout import indinvest_layout
from layouts.timehoriz_layout import timehoriz_layout
from layouts.market_layout import market_layout
from layouts.contact_layout import contact_layout

def register_callbacks(app):
    @app.callback(
        Output("page-content", "children"),
        Input("url", "pathname")
    )
    def display_page(pathname):

        if pathname == "/indinvest":
            return indinvest_layout()

        elif pathname == "/timehor":
            return timehoriz_layout()

        elif pathname == "/market":
            return market_layout()

        elif pathname == "/contact":
            return contact_layout()

        else:
            return home_layout()
