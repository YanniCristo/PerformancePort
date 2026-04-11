from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import logging
import stripe
import os

logger = logging.getLogger(__name__)

DATABASE_URL = os.getenv("DATABASE_URL")

if DATABASE_URL:
    # Compatibilità SQLAlchemy (Render usa postgres://)
    if DATABASE_URL.startswith("postgres://"):
        DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

else:
    # DB locale
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    DATABASE_URL = f"sqlite:///{os.path.join(BASE_DIR, 'db', 'users.db')}"

engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine)

# ── User helpers ──────────────────────────────────────────────────────────

def update_user_to_paid_by_id(user_id: int):
    from db.models import User
    
    db = SessionLocal()
    try:
        user = db.get(User, user_id)
        if user:
            user.is_paid = True
            db.commit()
    finally:
        db.close()

def set_stripe_customer_id(user_id: int, customer_id: str):
    from db.models import User
    
    db = SessionLocal()
    try:
        user = db.get(User, user_id)
        if user:
            user.stripe_customer_id = customer_id
            db.commit()
    finally:
        db.close()

def update_user_to_paid_by_stripe_customer(customer_id: str):
    from db.models import User

    db = SessionLocal()
    try:
        user = db.query(User).filter_by(stripe_customer_id=customer_id).first()
        if user:
            user.is_paid = True
            db.commit()
            logger.info(f"Utente {user.id} marcato come paid via customer {customer_id}")
        else:
            logger.warning(f"Nessun utente trovato per customer_id: {customer_id}")
    finally:
        db.close()

# ── Payment helpers ───────────────────────────────────────────────────────

def save_payment(session):
    """Inserisce o aggiorna un pagamento Stripe nel DB."""
    from db.models import Payment

    db = SessionLocal()
    try:
        email = None
        if session.customer_details and session.customer_details.email:
            email = session.customer_details.email

        existing = db.get(Payment, session.id)
        if existing:
            existing.amount = session.amount_total
            existing.status = session.payment_status
            existing.email = email
            existing.payment_intent = session.payment_intent
        else:
            db.add(Payment(
                id=session.id,
                amount=session.amount_total,
                status=session.payment_status,
                email=email,
                payment_intent=session.payment_intent,
            ))
        db.commit()
        logger.info(f"Pagamento salvato/aggiornato: {session.id} → {session.payment_status}")
    finally:
        db.close()


def save_subscription(subscription):
    """Salva o aggiorna un abbonamento Stripe nel DB."""
    from db.models import Subscription

    customer = stripe.Customer.retrieve(subscription.customer)
    email = customer.email

    db = SessionLocal()
    try:
        existing = db.get(Subscription, subscription.id)
        price_id = subscription["items"]["data"][0]["price"]["id"]
        period_end = subscription["items"]["data"][0]["current_period_end"]

        if existing:
            existing.status = subscription.status
            if email:
                existing.email = email
        else:
            db.add(Subscription(
                subscription_id=subscription.id,
                customer_id=subscription.customer,
                email=email,
                status=subscription.status,
                price_id=price_id,
                current_period_end=period_end,
            ))
        db.commit()
        logger.info(f"Subscription salvata: {subscription.id} → {subscription.status}")
    finally:
        db.close()


def event_exists(event_id: str) -> bool:
    """Controlla idempotenza: l'evento Stripe è già stato processato?"""
    from db.models import StripeEvent

    db = SessionLocal()
    try:
        return db.get(StripeEvent, event_id) is not None
    finally:
        db.close()


def save_event(event_id: str, event_type: str):
    """Registra un evento Stripe (per idempotenza)."""
    from db.models import StripeEvent

    db = SessionLocal()
    try:
        if not db.get(StripeEvent, event_id):
            db.add(StripeEvent(event_id=event_id, type=event_type))
            db.commit()
    finally:
        db.close()


def get_payment_by_id(session_id: str):
    """Restituisce il pagamento come dict, o None se non trovato."""
    from db.models import Payment

    db = SessionLocal()
    try:
        payment = db.get(Payment, session_id)
        if payment is None:
            return None
        return {
            "id": payment.id,
            "amount": payment.amount,
            "status": payment.status,
            "email": payment.email,
            "payment_intent": payment.payment_intent,
            "created_at": payment.created_at,
        }
    finally:
        db.close()
