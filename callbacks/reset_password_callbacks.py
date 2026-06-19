import dash_bootstrap_components as dbc
from dash import Input, Output, State, no_update
from db.database import SessionLocal
from db.models import User
from auth.utils import hash_password
from datetime import datetime, timezone


def register(app):

    @app.callback(
        Output("rp-feedback",         "children"),
        Output("rp-submit-btn",       "disabled"),
        Output("rp-new-password",     "value"),
        Output("rp-confirm-password", "value"),

        Input("rp-submit-btn", "n_clicks"),

        State("rp-token-store",       "data"),
        State("rp-new-password",      "value"),
        State("rp-confirm-password",  "value"),

        prevent_initial_call=True,
    )
    def handle_reset_password(n_clicks, token, password, confirm):

        # ── Validazione input ─────────────────────────────────────────────────
        if not password or len(password) < 6:
            return _alert("Password must be at least 6 characters long.", "danger"), False, no_update, no_update

        if password != confirm:
            return _alert("Passwords do not match.", "danger"), False, no_update, no_update

        if not token:
            return _alert("Invalid reset token. Please request a new link.", "danger"), True, no_update, no_update

        # ── Verifica token nel DB ─────────────────────────────────────────────
        db = SessionLocal()
        try:
            user = db.query(User).filter_by(reset_password_token=token).first()

            if not user:
                return _alert("This link is invalid or has already been used.", "danger"), True, no_update, no_update

            # Controllo scadenza
            if user.reset_token_expiry:
                expiry = user.reset_token_expiry
                if expiry.tzinfo is None:
                    expiry = expiry.replace(tzinfo=timezone.utc)
                if datetime.now(timezone.utc) > expiry:
                    return _alert("This reset link has expired. Please request a new one.", "warning"), True, no_update, no_update

            # ── Aggiorna la password e invalida il token ──────────────────────
            user.password_hash        = hash_password(password)
            user.reset_password_token = None
            user.reset_token_expiry   = None
            db.commit()

            return _alert("✓ Password updated! You can now log in.", "success"), True, "", ""

        except Exception as e:
            db.rollback()
            return _alert(f"An error occurred: {str(e)}", "danger"), False, no_update, no_update

        finally:
            db.close()


# ── Helper ────────────────────────────────────────────────────────────────────

def _alert(message: str, color: str):
    return dbc.Alert(message, color=color, className="rp-alert")
