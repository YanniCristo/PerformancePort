from dash import html
import dash_bootstrap_components as dbc

def model_port():
    return dbc.DropdownMenu(
        label="MODEL PORTFOLIOS",
        nav=True,
        in_navbar=True,
        children=[
            dbc.DropdownMenuItem("Asset Allocation", href="/"),
            dbc.DropdownMenuItem("Bond Strategies", href="/"),
            dbc.DropdownMenuItem("Equity Strategies", href="/equitystrat"),
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

def lang_view():
    LANGUAGES = [
        {"code": "us", "label": "US"},
        {"code": "en", "label": "EN"},
        {"code": "it", "label": "IT"},
        {"code": "es", "label": "ES"},
        {"code": "fr", "label": "FR"},
        {"code": "de", "label": "DE"},
        {"code": "ru", "label": "RU"}]
    
    return dbc.DropdownMenu(
        label=html.Span([
            html.Img(id="lang-flag-active", src="/assets/contents/flags/us.svg", className="lang-flag"),
            html.Span("US", id="lang-label-active", className="lang-label"),
        ], className="lang-dropdown-label"),
        nav=True,
        in_navbar=True,
        align_end=True,
        id="lang-dropdown",
        className="lang-dropdown",
        children=[
            dbc.DropdownMenuItem(
                html.Span([
                    html.Img(src=f"/assets/contents/flags/{lang['code']}.svg", className="lang-flag"),
                    html.Span(lang["label"]),
                ], className="lang-option-inner"), id=f"lang-{lang['code']}", n_clicks=0,
            )
            for lang in LANGUAGES
        ],
    )
