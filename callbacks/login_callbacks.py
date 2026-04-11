from dash import Input, Output, State, no_update, ctx
from auth.utils import verify_password, hash_password
from utils.functions import send_verification_email_Brevo
from sqlalchemy.exc import IntegrityError
from dash.exceptions import PreventUpdate
from db.database import SessionLocal
from flask_login import login_user
from db.models import User
import secrets

def register(app):

    @app.callback(
        Output("login-modal", "is_open"),
        Output("signup-modal", "is_open"),
        Output("auth-event", "data"),
        Output("login-feedback", "children"),
        Output("signup-feedback", "children"),
        
        Input("start-btn", "n_clicks"),
        Input("open-signup-btn", "n_clicks"),
        Input("back-to-login-btn", "n_clicks"),
        Input("login-btn", "n_clicks"),
        Input("signup-btn", "n_clicks"),
        
        State("login-modal", "is_open"),
        State("signup-modal", "is_open"),
        
        State("login-email", "value"),
        State("login-password", "value"),

        State("signup-Email", "value"),
        State("signup-username", "value"),
        State("signup-password", "value"),
        State("signup-password-confirm", "value"),
        State("auth-event", "data"),
        
        prevent_initial_call=True
    )
    def handle_auth_modal(start_click,
                          open_signup_click,
                          back_to_login_click,
                          login_click,
                          signup_click,

                          login_open,
                          signup_open,

                          login_email,
                          login_password,

                          signup_email,
                          signup_username,
                          signup_password,
                          signup_password_confirm,

                          auth_event):

        # Salvo il trigger della funzione
        trigger = ctx.triggered_id

        # valori default
        login_is_open = login_open
        signup_is_open = signup_open
        login_feedback = no_update
        signup_feedback = no_update
        auth_data = auth_event

        # -----------------------------
        # Apri login modal
        if trigger == "start-btn":
            if not start_click:
                raise PreventUpdate
            return True, False, auth_data, "", ""

        # -----------------------------
        # Passa da login a signup
        if trigger == "open-signup-btn":
            return False, True, auth_data, "", ""

        # -----------------------------
        # Torna da signup a login
        if trigger == "back-to-login-btn":
            return True, False, auth_data, "", ""

        # -----------------------------
        # Login utente
        if trigger == "login-btn":
            if not login_click:
                raise PreventUpdate
            
            if not login_email or not login_password:
                return True, False, auth_data, "Insert both email and password.", ""

            db = SessionLocal()
            try:
                # Controllo esistenza user in db
                user = db.query(User).filter_by(email=login_email.strip()).first()

                if user and verify_password(user.password_hash, login_password):

                    # Check utente verificato
                    if not user.is_verified:
                        return True, False, auth_data, "Please verify your email first.", ""
                    
                    login_user(user)
                    return False, False, auth_data + 1, "", ""

                return True, False, auth_data, "No user found.", ""

            finally:
                db.close()

            raise PreventUpdate

        # -----------------------------
        # Registrazione utente
        if trigger == "signup-btn":

            fields = [signup_username, signup_password, signup_password_confirm, signup_email]
            if not all(fields):
                return False, True, auth_data, "", "All fields must be compiled."

            signup_username = signup_username.strip()

            if len(signup_username) < 5:
                return False, True, auth_data, "", "Username must be at least 5 characters long."

            if len(signup_password) < 6:
                return False, True, auth_data, "", "Password must be at least 6 characters long."

            if signup_password != signup_password_confirm:
                return False, True, auth_data, "", "Passwords do not match."

            db = SessionLocal()
            try:
                existing_user = db.query(User).filter_by(username=signup_username).first()
                existing_email = db.query(User).filter_by(email=signup_email).first()
                if existing_user:
                    return False, True, auth_data, "", "Username already exist."
                if existing_email:
                    return False, True, auth_data, "", "Email already exist."

                # Genero token e salvo utente non verificato
                token = secrets.token_urlsafe(32)
                new_user = User(
                    email=signup_email,
                    username=signup_username,
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
                return True, False, auth_data, txt, ""

            except IntegrityError:
                db.rollback()
                return False, True, auth_data, "", "Username already exist."

            except Exception as e:
                db.rollback()
                return False, True, auth_data, "", f"Registration error: {str(e)}"

            finally:
                db.close()

        return login_is_open, signup_is_open, auth_data, login_feedback, signup_feedback
