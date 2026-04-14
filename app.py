import dash_bootstrap_components as dbc
from flask_login import LoginManager
from flask import Flask
from dash import Dash
import stripe

# 0. Carico variabili d'ambiente
from dotenv import load_dotenv
load_dotenv()

from auth.routes import init_auth_routes
from db.database import SessionLocal, engine
from db.models import User, Payment, StripeEvent, Subscription, Base

from payments.routes import payment_bp

from callbacks import register_all_callbacks
from layouts.main_layout import main_layout
import os

# 1. Crea server Flask
server = Flask(__name__)
server.secret_key = os.getenv("SECRET_KEY", "dev-key")

# Imposta Stripe api_key
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

# 2. Inizializza Flask-Login
login_manager = LoginManager()
login_manager.init_app(server)

# 3. User_loader
@login_manager.user_loader
def load_user(user_id):
    db = SessionLocal()
    try:
        return db.get(User, int(user_id))
    finally:
        db.close()

# 4. Inizializzo database
Base.metadata.create_all(bind=engine) #DA RIVEDERE IN PRODUZIONE

# 5. Redirect utenti non autorizzati
@login_manager.unauthorized_handler
def unauthorized():
    from flask import redirect
    return redirect("/")

# 6. Inizializza routes auth
init_auth_routes(server)

# 7. Registra le route Stripe
server.register_blueprint(payment_bp)

# 7. Crea app Dash
app = Dash(
    __name__,
    server=server,
    title="PerformingPort.com",
    external_stylesheets=[dbc.themes.CYBORG],
    update_title=None)

# 8. Importo le callbacks e creo main layout
register_all_callbacks(app)
app.layout = main_layout()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 9000))
    app.run(debug=False, host="0.0.0.0", port=port)
