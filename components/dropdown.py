from dash import html
import dash_bootstrap_components as dbc

def model_port():

    return dbc.DropdownMenu(
        label="MODEL PORTFOLIOS",
        nav=True,
        in_navbar=True,
        children=[
            dbc.DropdownMenuItem("Equity Strategies", href="/"),
            dbc.DropdownMenuItem("Bond Strategies", href="/"),
            dbc.DropdownMenuItem("Asset Allocation", href="/"),
            ],
        )

def mkt_view():

    return dbc.DropdownMenu(
        label="MARKET VIEW",
        nav=True,
        in_navbar=True,
        children=[
            dbc.DropdownMenuItem("Economic Overview", href="/"),
            dbc.DropdownMenuItem("Market Phase", href="/"),
            dbc.DropdownMenuItem("Macro Allocation", href="/"),
            dbc.DropdownMenuItem("Leading Equity Markets Allocation", href="/"),
            ],
        )
