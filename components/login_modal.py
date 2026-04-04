import dash_bootstrap_components as dbc
from dash import html

def login_modal():
    return dbc.Modal(
            [
                dbc.ModalHeader(dbc.ModalTitle("Login")),
                dbc.ModalBody([
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
                    html.P("Don't have an account?"),
                    dbc.Button("Sign up", id="open-signup-btn", color="secondary", className="w-100")
                ]),
            ],
            id="login-modal",
            is_open=False,
        )
