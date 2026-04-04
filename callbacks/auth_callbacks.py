from dash import Output, Input, html
from flask_login import current_user
import dash_bootstrap_components as dbc

def register(app):

    @app.callback(
        Output("user-status", "children"),
        Input("url", "pathname"),  # trigger quando cambia pagina
        Input("auth-event", "data") # trigger quando si effettua login
    )
    def update_user_status(_pathname, _auth_event):

        if current_user.is_authenticated:
            username = current_user.email
            initials = username[:2].upper()

            return html.Div(
                [
                    dbc.DropdownMenu(
                        label=initials,
                        children=[
                            dbc.DropdownMenuItem(f"Logged as {username}", header=True),
                            dbc.DropdownMenuItem(divider=True),
                            dbc.DropdownMenuItem("Logout", href="/logout", external_link=True),
                        ],
                        color="primary",
                        className="rounded-circle",
                        toggle_style={
                            "width": "40px", "height": "40px",
                            "borderRadius": "50%", "padding": "0",
                            "textAlign": "center", "fontWeight": "bold"
                        }
                    )
                ]
            )

        return dbc.Button(
            ["Start now", html.Span("→", className="cta-icon")],
            id="start-btn", color="primary",
            className="cta-dg cta-dg-primary-white cta-dg-with-icon")
