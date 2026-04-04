from dash import html
import dash_bootstrap_components as dbc

def model_port():
    return dbc.DropdownMenu(
        label="MODEL PORTFOLIOS",
        nav=True,
        in_navbar=True,
        children=[
            dbc.DropdownMenuItem("Asset Allocation", href="/"),
            dbc.DropdownMenuItem("Equity Strategies", href="/equitystrat"),
            dbc.DropdownMenuItem("Bond Strategies", href="/")
            ],
        )

def mkt_view():
    return dbc.DropdownMenu(
        label="MARKET VIEW",
        nav=True,
        in_navbar=True,
        children=[
            dbc.DropdownMenuItem("Economic Overview", href="/ecoview"),
            dbc.DropdownMenuItem("Market Phase", href="/marketphase"),
            dbc.DropdownMenuItem("Macro Allocation", href="/macroall")
            ])
