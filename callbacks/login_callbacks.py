from dash import Input, Output, State, no_update, ctx, html
from auth.utils import verify_password, hash_password
from utils.functions import send_verification_email_Brevo, send_reset_password_email_Brevo
from sqlalchemy.exc import IntegrityError
from dash.exceptions import PreventUpdate
from db.database import SessionLocal
from flask_login import login_user
from db.models import User
from datetime import datetime, timezone, timedelta
import secrets

def register(app):

    # ──────────────────────────────────────────────────────────────────────────
    # Callback principale: login / signup / forgot password
    @app.callback(
        Output("login-modal",               "is_open"),
        Output("signup-modal",              "is_open"),
        Output("auth-event",                "data"),
        Output("login-feedback",            "children"),
        Output("signup-feedback",           "children"),

        # Visibilità sezioni nella login modal
        Output("login-form-section",        "style"),
        Output("forgot-password-section",   "style"),

        # Feedback forgot password
        Output("forgot-password-feedback",  "children"),
        
        Input("start-btn",                  "n_clicks"),
        Input("open-signup-btn",            "n_clicks"),
        Input("back-to-login-btn",          "n_clicks"),
        Input("login-btn",                  "n_clicks"),
        Input("signup-btn",                 "n_clicks"),

        # Forgot password triggers
        Input("open-forgot-password-btn",   "n_clicks"),
        Input("back-from-forgot-btn",       "n_clicks"),
        Input("send-reset-btn",             "n_clicks"),
        
        State("login-modal",                "is_open"),
        State("signup-modal",               "is_open"),
        
        State("login-email",                "value"),
        State("login-password",             "value"),

        State("signup-Email",               "value"),
        State("signup-password",            "value"),
        State("signup-password-confirm",    "value"),
        State("auth-event",                 "data"),

        State("forgot-password-email",      "value"),
        
        prevent_initial_call=True
    )
    def handle_auth_modal(start_click,
                          open_signup_click,
                          back_to_login_click,
                          login_click,
                          signup_click,

                          open_forgot_click,
                          back_from_forgot_click,
                          send_reset_click,

                          login_open,
                          signup_open,

                          login_email,
                          login_password,

                          signup_email,
                          signup_password,
                          signup_password_confirm,

                          auth_event,

                          forgot_email):

        # Salvo il trigger della funzione
        trigger = ctx.triggered_id

        # Stili default
        SHOW = {"display": "block"}
        HIDE = {"display": "none"}
 
        # Valori default (non aggiornare se non necessario)
        login_is_open      = login_open
        signup_is_open     = signup_open
        login_feedback     = no_update
        signup_feedback    = no_update
        auth_data          = auth_event
        forgot_feedback    = no_update
        login_sec_style    = no_update
        forgot_sec_style   = no_update

        # -----------------------------
        # Apri login modal
        if trigger == "start-btn":
            if not start_click:
                raise PreventUpdate
            return True, False, auth_event, "", "", SHOW, HIDE, ""

        # -----------------------------
        # Passa da login a signup
        if trigger == "open-signup-btn":
            return False, True, auth_event, "", "", SHOW, HIDE, ""

        # -----------------------------
        # Torna da signup a login
        if trigger == "back-to-login-btn":
            return True, False, auth_event, "", "", SHOW, HIDE, ""

        # ------------------------------------------------------------------
        # Apri sezione "Forgot password" (dentro la login modal)
        if trigger == "open-forgot-password-btn":
            return True, False, auth_event, "", "", HIDE, SHOW, ""
 
        # ------------------------------------------------------------------
        # Torna alla login form dal forgot password
        if trigger == "back-from-forgot-btn":
            return True, False, auth_event, "", "", SHOW, HIDE, ""

        # -----------------------------
        # Login utente
        if trigger == "login-btn":
            if not login_click:
                raise PreventUpdate
            
            if not login_email or not login_password:
                return True, False, auth_event, "Insert both email and password.", "", SHOW, HIDE, ""

            db = SessionLocal()
            try:
                # Controllo esistenza user in db
                user = db.query(User).filter_by(email=login_email.strip()).first()

                if user and verify_password(user.password_hash, login_password):

                    # Check utente verificato
                    if not user.is_verified:
                        return True, False, auth_event, "Please verify your email first.", "", SHOW, HIDE, ""
                    
                    login_user(user)
                    return False, False, auth_event + 1, "", "", SHOW, HIDE, ""

                return True, False, auth_event, "No user found.", "", SHOW, HIDE, ""

            finally:
                db.close()
        

        # -----------------------------
        # Registrazione utente
        if trigger == "signup-btn":

            fields = [signup_password, signup_password_confirm, signup_email]
            if not all(fields):
                return False, True, auth_event, "", "All fields must be compiled.", SHOW, HIDE, ""

            if len(signup_password) < 6:
                return False, True, auth_event, "", "Password must be at least 6 characters long.", SHOW, HIDE, ""

            if signup_password != signup_password_confirm:
                return False, True, auth_event, "", "Passwords do not match.", SHOW, HIDE, ""

            db = SessionLocal()
            try:
                existing_email = db.query(User).filter_by(email=signup_email).first()
                if existing_email:
                    return False, True, auth_event, "", "Email already exist.", SHOW, HIDE, ""

                # Genero token e salvo utente non verificato
                token = secrets.token_urlsafe(32)
                new_user = User(
                    email=signup_email,
                    password_hash=hash_password(signup_password),
                    is_verified=False,
                    verification_token=token)

                db.add(new_user)
                db.commit()
                db.refresh(new_user)

                try:
                    send_verification_email_Brevo(signup_email, token)
                except Exception as e:
                    print("Email fallita:", e)

                txt="A confirmation email has been sent. Please click the link in the email to complete your registration."
                return True, False, auth_event, txt, "", SHOW, HIDE, ""

            except IntegrityError:
                db.rollback()
                return False, True, auth_event, "", "Username already exist.", SHOW, HIDE, ""

            except Exception as e:
                db.rollback()
                return False, True, auth_event, "", f"Registration error: {str(e)}", SHOW, HIDE, ""

            finally:
                db.close()

        # ------------------------------------------------------------------
        # Reset password: invio email con link
        if trigger == "send-reset-btn":
            if not send_reset_click:
                raise PreventUpdate

            if not forgot_email or not forgot_email.strip():
                return (True, False, auth_event, "", "", HIDE, SHOW,
                        _feedback_danger("Please enter your email address."))

            db = SessionLocal()
            try:
                user = db.query(User).filter_by(email=forgot_email.strip()).first()

                # Risposta generica per sicurezza (non rivela se la mail esiste)
                generic_msg = _feedback_success(
                    "If this email is registered, you will receive a password reset link shortly.")

                if user:
                    # Genero token con scadenza 1 ora
                    reset_token = secrets.token_urlsafe(32)
                    user.reset_password_token = reset_token
                    user.reset_token_expiry = datetime.now(timezone.utc) + timedelta(hours=1)
                    db.commit()
 
                    try:
                        send_reset_password_email_Brevo(user.email, reset_token)
                    except Exception as e:
                        print("Reset email fallita:", e)
 
                return (True, False, auth_event, "", "", HIDE, SHOW, generic_msg)
 
            finally:
                db.close()
        
        return (login_is_open, signup_is_open, auth_event,
                login_feedback, signup_feedback,
                login_sec_style, forgot_sec_style, forgot_feedback)


# ──────────────────────────────────────────────────────────────────────────────
# Helper UI feedback
# ──────────────────────────────────────────────────────────────────────────────
def _feedback_danger(msg: str):
    return html.Div(msg, className="text-danger")
 
def _feedback_success(msg: str):
    return html.Div(msg, className="text-success")
