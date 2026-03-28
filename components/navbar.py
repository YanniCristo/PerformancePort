from dash import html
import dash_bootstrap_components as dbc
import components.dropdown as dd
import components.buttons as butt

def navbar():
    return dbc.Navbar(
        dbc.Container(
            [
                # Logo
                dbc.NavbarBrand(html.Img(src="/assets/contents/general/logo.png"), href="/"),

                # Hamburger toggle
                dbc.NavbarToggler(id="navbar-toggler"),

                # Collapse con link e pulsante
                dbc.Collapse(
                    dbc.Container(
                        [
                            # Sezione link a sinistra
                            dbc.Nav(
                                [
                                    dbc.NavLink("INDEPENDENCE", href="/indinvest"),
                                    dbc.NavLink("TIME HORIZON", href="/timehor"),
                                    dbc.NavLink("MARKET CYCLES", href="/market"),
                                    dd.mkt_view(),
                                    dd.model_port(),
                                    dbc.NavLink("HELP", href="/FAQ"),
                                ],
                                navbar=True,
                                className="flex-grow-1"
                            ),

                            # Sezione bottone a destra
                            butt.login(),
                        ],
                        className="d-flex flex-column flex-lg-row align-items-lg-center w-100"
                    ),
                    id="navbar-collapse",
                    is_open=False,
                    navbar=True,
                ),
            ],
            fluid=True,
            style={"paddingLeft": "8%", "paddingRight": "8%"},
            className="d-flex align-items-center"
        ),
        color="dark",
        dark=True,
        expand="lg",
        fixed="top",
        className="main-navbar"
    )
