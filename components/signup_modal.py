import dash_bootstrap_components as dbc
from dash import html

def signup_modal():
    return dbc.Modal(
        [
            dbc.ModalHeader(dbc.ModalTitle("Create account")),
            dbc.ModalBody([
                dbc.Input(
                    id="signup-Email",
                    placeholder="Email",
                    type="email",
                    className="mb-3"
                ),
                
                dbc.Input(
                    id="signup-username",
                    placeholder="Username",
                    type="text",
                    className="mb-3"
                ),
                
                dbc.Input(
                    id="signup-password",
                    placeholder="Password",
                    type="password",
                    className="mb-3"
                ),
                
                dbc.Input(
                    id="signup-password-confirm",
                    placeholder="Confirm password",
                    type="password",
                    className="mb-3"
                ),

                html.Div(id="signup-feedback", className="text-danger mb-3"),

                dbc.Button("Create account", id="signup-btn", color="success", className="w-100"),
                html.Hr(),
                dbc.Button("Back to login", id="back-to-login-btn", color="secondary", className="w-100")
                
            ]),
        ],
        id="signup-modal",
        is_open=False,
    )
