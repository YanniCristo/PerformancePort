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
            email = current_user.email
            initials = email[:2].upper()

            # Creo struttura della pagina
            children = [
                dbc.DropdownMenu(
                    label=initials,
                    children=[
                        dbc.DropdownMenuItem(f"{email}", header=True),
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
                ),
            ]
            
            # Mostra "Upgrade now" solo se l'utente non ha ancora pagato
            if not current_user.is_paid:
                children.append(
                    dbc.Button(
                        ["Upgrade now", html.Span("→", className="cta-icon")],
                        id="pay-btn-10", color="primary",
                        className="cta-dg cta-dg-primary-white cta-dg-with-icon"
                    )
                )
            else:
                children.append(
                    html.Span("PRO", title="Premium", style={
                        "fontSize": "10px",
                        "fontWeight": "bold",
                        "color": "#FFD700",
                        "border": "1px solid #FFD700",
                        "borderRadius": "4px",
                        "padding": "2px 5px",
                        "letterSpacing": "0.5px"
                    })
                )
                

            return html.Div(
                children,
                style={
                    "display": "flex",
                    "flexDirection": "row",
                    "alignItems": "center",
                    "gap": "15px"
                }
            )

        return dbc.Button(
            ["Start now", html.Span("→", className="cta-icon")],
            id="start-btn", color="primary",
            className="cta-dg cta-dg-primary-white cta-dg-with-icon")
