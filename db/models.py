from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import declarative_base
from datetime import datetime, timezone
from flask_login import UserMixin
from db.database import engine

Base = declarative_base()

class User(UserMixin, Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    is_verified = Column(Boolean, default=False)
    is_paid = Column(Boolean, default=False)
    stripe_customer_id = Column(String, unique=True)
    verification_token = Column(String, nullable=True)
    
class Payment(Base):
    __tablename__ = "payments"

    id = Column(String, primary_key=True)          # Stripe checkout session ID
    amount = Column(Integer, nullable=False)
    status = Column(String, nullable=False)
    email = Column(String)
    payment_intent = Column(String)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))


class StripeEvent(Base):
    __tablename__ = "stripe_events"

    event_id = Column(String, primary_key=True)
    type = Column(String)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))


class Subscription(Base):
    __tablename__ = "subscriptions"

    subscription_id = Column(String, primary_key=True)
    customer_id = Column(String, nullable=False)
    email = Column(String)
    status = Column(String, nullable=False)
    price_id = Column(String)
    current_period_end = Column(Integer)           # unix timestamp
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

