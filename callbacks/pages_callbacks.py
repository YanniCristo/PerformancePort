from dash import Input, Output
from layouts.home_layout import home_layout
from layouts.indinvest_layout import indinvest_layout
from layouts.timehoriz_layout import timehoriz_layout
from layouts.market_layout import market_layout
from layouts.equity_strategy import equity_strategy
from layouts.eco_view import eco_view
from layouts.contact_layout import contact_layout
from layouts.FAQ import FAQ_layout
from layouts.macroallocation import macroallocation
from layouts.marketphase import marketphase


def register(app):
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

        elif pathname == "/FAQ":
            return FAQ_layout()

        elif pathname == "/equitystrat":
            return equity_strategy()

        elif pathname == "/marketphase":
            return marketphase()

        elif pathname == "/macroall":
            return macroallocation()
        
        elif pathname == "/ecoview":
            return eco_view()

        elif pathname == "/contact":
            return contact_layout()

        else:
            return home_layout()
