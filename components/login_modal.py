import dash_bootstrap_components as dbc
from dash import html

def login_modal():
    return dbc.Modal(
            [
                dbc.ModalHeader(dbc.ModalTitle("Login")),
                dbc.ModalBody([

                    # ── Login form ──────────────────────────────────
                    html.Div(id="login-form-section", style={"display": "block"}, children=[

                        dbc.Input(id="login-email",
                                  placeholder="Email",
                                  type="email",
                                  className="mb-3"),
                        
                        dbc.Input(id="login-password",
                                  placeholder="Password",
                                  type="password",
                                  className="mb-3"),

                        html.Div(id="login-feedback", className="text-danger mb-3"),
                        
                        dbc.Button("Login", id="login-btn", color="primary", className="w-100"),
                        html.Hr(),

                        html.P(["Forgot your password? ",
                                html.A("Reset it here",id="open-forgot-password-btn",href="#",
                                       className="text-info",style={"cursor": "pointer", "textDecoration": "underline"})
                            ], className="text-center mb-2"),

                        html.P("Don't have an account?"),
                        dbc.Button("Sign up", id="open-signup-btn", color="secondary", className="w-100"),
                        
                    ]),
                

                    # ── Forgot password form ───────────────────────
                    html.Div(id="forgot-password-section", style={"display": "none"}, children=[

                        html.P("Enter your email address and we'll send you a link to reset your password.",
                                   className="text-muted mb-3"),

                        dbc.Input(id="forgot-password-email", placeholder="Email",
                                      type="email", className="mb-3"),

                        html.Div(id="forgot-password-feedback", className="mb-3"),

                        dbc.Button("Send reset link", id="send-reset-btn",
                                   color="primary", className="w-100 mb-2"),
     
                        dbc.Button("Back to login", id="back-from-forgot-btn",
                                   color="secondary", outline=True, className="w-100"),
                    ]),
                ]),
            ],
            id="login-modal",
            is_open=False,
        )
