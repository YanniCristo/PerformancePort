from dash import html
import dash_bootstrap_components as dbc

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
                dbc.NavLink("Market Cycle", href="/market"),
                dbc.NavLink("Strategies", href="/strategies"),
                dbc.NavLink("Results", href="/results"),
                dbc.NavLink("Contact", href="/contact"),
            ], className="ms-auto",
                    style={'padding-right':'25px'})

        ], fluid=True),
        color="dark",
        dark=True
    )
