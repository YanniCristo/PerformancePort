from flask_login import logout_user
from flask import redirect, request
from db.database import SessionLocal
from auth.models import User

def init_auth_routes(server):

    @server.route("/logout")
    def logout():
        logout_user()
        return redirect("/")

    @server.route("/verify")
    def verify_email():
        token = request.args.get("token")

        if not token:
            return "Token mancante"

        db = SessionLocal()
        try:
            user = db.query(User).filter_by(verification_token=token).first()

            if not user:
                return "Token non valido"

            user.is_verified = True
            user.verification_token = None
            db.commit()

            return "Account verificato! Ora puoi fare login."

        finally:
            db.close()
