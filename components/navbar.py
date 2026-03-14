from dash import html
import dash_bootstrap_components as dbc
import components.dropdown as dd

def navbar():

    return dbc.Navbar(
        dbc.Container([

            dbc.NavbarBrand(
                html.Img(
                    src="/assets/logo.png",
                    style={"height": "50px"}
                ),
                href="/",
                style={'padding-left':'25px'}
            ),

            dbc.Nav([
                dbc.NavLink("Home", href="/"),
                dbc.NavLink("Indipendent Investing", href="/indinvest"),
                dbc.NavLink("Time Horizon", href="/timehor"),
                dbc.NavLink("Market Cycles", href="/market"),

                dd.mkt_view(),
                dd.model_port(),
         
                dbc.NavLink("Contact", href="/contact"),
                
            ], className="ms-auto",
                    style={'padding-right':'25px'})

        ], fluid=True),
        color="dark",
        dark=True
    )
