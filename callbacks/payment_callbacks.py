from flask_login import current_user
import logging, os
import stripe
from dash import Input, Output, no_update, ctx
from payments.stripe_service import create_checkout_session, create_subscription_session

logger = logging.getLogger(__name__)

def register(app):

    @app.callback(
        Output("redirect", "href"), # dcc.Location(id="url", refresh=True)
        Output("checkout-session", "data"),

        Input("pay-btn-10", "n_clicks"),
##        Input("subscribe-btn", "n_clicks"),
        
        prevent_initial_call=True
    )
    def start_payment(n1):#, n_sub):
        # Blocca esecuzioni spurie al mount del componente
        if not any([n1]):#, n_sub]):
            return no_update, no_update
        
        user_id = current_user.id if current_user.is_authenticated else None
        
        try:
            triggered = ctx.triggered_id

            if triggered == "subscribe-btn":
                price_id = os.getenv("STRIPE_MONTHLY_PRICE_ID")
                session = create_subscription_session(price_id, user_id)
            else:
                # Salvo il trigger della funzione
                amount = int(ctx.triggered_id.split("-")[-1]) * 100
                session = create_checkout_session(amount, user_id)
            
            # Faccio redirect a url Stripe per far procedere al pagamento
            return session["url"], {"session_id": session["session_id"]}
        
        except stripe.error.StripeError as e:
            logger.error(f"Errore Stripe: {e}")
            return no_update, no_update
        except Exception as e:
            logger.error(f"Errore imprevisto: {e}")
            return no_update, no_update
