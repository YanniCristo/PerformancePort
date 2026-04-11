import os
import logging
import stripe

logger = logging.getLogger(__name__)


def create_checkout_session(amount: int, user_id: int) -> dict:
    DOMAIN = os.getenv("DOMAIN")

    # Dico a Stripe: crea una sessione di pagamento ospitata da te
    session = stripe.checkout.Session.create(
        client_reference_id=str(user_id),
        payment_method_types=["card"],
        line_items=[{
            "price_data": {
                "currency": "eur",
                "product_data": {"name": "Prodotto demo"},
                "unit_amount": amount
            },
            "quantity": 1,
        }],
        mode="payment", # Pagamento singolo (no abbonamento)
        success_url=f"{DOMAIN}/success?session_id={{CHECKOUT_SESSION_ID}}",
        cancel_url=f"{DOMAIN}/cancel", # Fallback se utente annulla
    )

    # Stripe sostituisce {CHECKOUT_SESSION_ID} e ritorna ID della session
    logger.info(f"Checkout session creata: {session.id} ({amount} centesimi)")
    return {"url": session.url, "session_id": session.id}


def create_subscription_session(price_id: str, user_id: int) -> dict:
    """
    Crea una Checkout Session per abbonamento mensile.
    price_id deve essere un Price ricorrente creato su Stripe Dashboard
    (es. "price_1ABC...").
    """
    DOMAIN = os.getenv("DOMAIN")
    session = stripe.checkout.Session.create(
        client_reference_id=str(user_id),
        payment_method_types=["card"],
        line_items=[{
            "price": price_id,   # Price ID da Stripe, NON price_data inline
            "quantity": 1,
        }],
        mode="subscription",    # ← chiave: abbonamento, non pagamento singolo
        success_url=f"{DOMAIN}/success?session_id={{CHECKOUT_SESSION_ID}}",
        cancel_url=f"{DOMAIN}/cancel",
    )
    logger.info(f"Subscription session creata: {session.id} (price: {price_id})")
    return {"url": session.url, "session_id": session.id}


def retrieve_checkout_session(session_id):
    """
    Recupera una Checkout Session da Stripe.
    Lancia stripe.error.StripeError se session_id non valido.
    """
    return stripe.checkout.Session.retrieve(session_id)
