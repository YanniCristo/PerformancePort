import dash_bootstrap_components as dbc
from dash import html, dcc


def reset_password_layout(token: str = None, lang: str = "en"):
    """
    Layout Dash per la pagina di reset password.
    Riceve il token dall'URL (passato da pages_callbacks).

    Stati possibili:
    - token=None  → card di errore (link mancante/malformato)
    - token valido → form nuova password (validazione nel callback)
    """

    if not token:
        return _page_wrapper(_error_card(
            "Invalid link",
            "The reset link is missing or malformed. Please request a new one."
        ))

    return _page_wrapper(
        dbc.Card([
            dbc.CardBody([

                html.Div("🔑", className="rp-icon"),

                html.H2("Reset your password", className="rp-title"),
                html.P(
                    "Choose a new password for your account. It must be at least 6 characters.",
                    className="rp-subtitle"
                ),

                dbc.Input(
                    id="rp-new-password",
                    type="password",
                    placeholder="New password",
                    className="mb-3 rp-input",
                    autocomplete="new-password",
                ),
                dbc.Input(
                    id="rp-confirm-password",
                    type="password",
                    placeholder="Confirm new password",
                    className="mb-3 rp-input",
                    autocomplete="new-password",
                ),

                # Feedback errore / successo dal callback
                html.Div(id="rp-feedback", className="mb-3"),

                # Token passato al callback senza esporlo nell'URL
                dcc.Store(id="rp-token-store", data=token),

                dbc.Button(
                    [html.I(className="bi bi-shield-lock-fill me-2"), "Set new password"],
                    id="rp-submit-btn",
                    color="primary",
                    className="w-100 rp-btn",
                    n_clicks=0,
                ),

                html.Hr(className="rp-divider"),

                dbc.Button(
                    [html.I(className="bi bi-house-fill me-2"), "Back to homepage"],
                    href="/",
                    color="dark",
                    outline=True,
                    className="w-100 rp-btn-secondary",
                    external_link=True,
                ),

            ])
        ], className="rp-card"),
        token=token,
    )


# ── Helpers ───────────────────────────────────────────────────────────────────

def _page_wrapper(content, token=None):
    """Wrapper pagina. Il secondo dcc.Store serve solo nel ramo form (token presente)."""
    return html.Div([
        html.Div(content, className="rp-card-wrapper"),
    ], className="rp-page")


def _error_card(title: str, message: str):
    return dbc.Card([
        dbc.CardBody([
            html.Div("⚠️", className="rp-icon rp-icon--error"),
            html.H2(title, className="rp-title"),
            html.P(message, className="rp-subtitle"),
            html.Hr(className="rp-divider"),
            dbc.Button(
                [html.I(className="bi bi-house-fill me-2"), "Back to homepage"],
                href="/",
                color="dark",
                outline=True,
                className="w-100 rp-btn-secondary",
                external_link=True,
            ),
        ])
    ], className="rp-card rp-card--error")
