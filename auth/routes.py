from flask_login import logout_user
from flask import redirect, request
from db.database import SessionLocal
from db.models import User

def init_auth_routes(server):

    @server.route("/logout")
    def logout():
        logout_user()
        return redirect("/")

    @server.route("/verify")
    def verify_email():
        token = request.args.get("token")

        if not token:
            return "Missing Token"

        db = SessionLocal()
        try:
            user = db.query(User).filter_by(verification_token=token).first()

            if not user:
                return "Invalid Token"

            user.is_verified = True
            user.verification_token = None
            db.commit()

            return "Account verified! You can now log in."

        finally:
            db.close()
