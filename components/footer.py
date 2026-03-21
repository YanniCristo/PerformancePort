import dash
from dash import html
import dash_bootstrap_components as dbc

def footer():
        
        return html.Footer(
                dbc.Container([
                        dbc.Row([

                            # CONTATTI
                            dbc.Col([
                                html.H5("CONTACT", className="footer-title"),

                                html.P([
                                    html.Strong("PerformingPort S.r.l."),
                                    html.Br(),
                                    "Via Roma 45",
                                    html.Br(),
                                    "20121 Trieste (TS), Italia",
                                    html.Br(),
                                    "Tel. +39 02 1234567",
                                    html.Br(),
                                    "info@ppconsulting.it"
                                ]),

                                html.Br(),

                                html.Div([
                                    html.A("LinkedIn", href="#", className="social"),
                                    html.A("YouTube", href="#", className="social"),
                                    html.A("Facebook", href="#", className="social"),
                                    html.A("Instagram", href="#", className="social"),
                                ])

                            ], md=3),

                            # COLONNA PP
                            dbc.Col([
                                html.H5("PERFORMINGPORT", className="footer-title"),

                                html.Ul([
                                    html.Li(html.A("About us", href="#")),
                                    html.Li(html.A("Contact", href="/contact")),
                                    html.Li(html.A("Blog", href="#")),
                                    html.Li(html.A("Events", href="#")),
                                    html.Li(html.A("Work with us", href="#")),
                                ])
                            ], md=3),

                            # SERVIZI
                            dbc.Col([
                                html.H5("CONSULTANCY", className="footer-title"),

                                html.Ul([
                                    html.Li(html.A("Financial Analisys", href="#")),
                                    html.Li(html.A("Investments", href="#")),
                                    html.Li(html.A("Financial plan", href="#")),
                                    html.Li(html.A("Retirement planning", href="#")),
                                ]),

                            ], md=3),

                            # NEWSLETTER
                            dbc.Col([
                                html.H5("NEWSLETTER", className="footer-title"),

                                dbc.Input(
                                    placeholder="E-mail",
                                    type="email",
                                    className="mb-2"
                                ),

                                dbc.Button(
                                    "Send",
                                    color="primary",
                                    className="mb-2"
                                ),

                                html.Div([
                                    dbc.Checkbox(id="privacy"),
                                    html.Span(
                                        " I have read the Privacy Policy and I consent "
                                        " to receive the newsletter. "
                                    )
                                ], className="privacy-text")

                            ], md=3)

                        ]),

                        html.Hr(),

                        html.Div(
                            "© 2026 PerformingPort S.r.l. – All right reserved.",
                            style={"textAlign": "center"}
                        )

                    ], fluid=True),

                    className="footer"
                )
