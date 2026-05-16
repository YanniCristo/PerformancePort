from sqlalchemy import Column, Integer, String, Boolean, DateTime, Float, Date, UniqueConstraint
from sqlalchemy.orm import declarative_base
from datetime import datetime, timezone
from flask_login import UserMixin
from db.database import engine

Base = declarative_base()

# ──────────────────────────────────────────────────────────────────────────────
# ── Users data ───────────────────────────────────────────────────────────────

class User(UserMixin, Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    signin_date = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    is_verified = Column(Boolean, default=False)
    is_paid = Column(Boolean, default=False)
    stripe_customer_id = Column(String, unique=True)
    verification_token = Column(String, nullable=True)
    
class Payment(Base):
    __tablename__ = "payments"

    username = Column(String, unique=False, nullable=True)
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

    username = Column(String, unique=False, nullable=True)
    subscription_id = Column(String, primary_key=True)
    customer_id = Column(String, nullable=False)
    email = Column(String)
    status = Column(String, nullable=False)
    price_id = Column(String)
    current_period_end = Column(Integer) # unix timestamp
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))


# ──────────────────────────────────────────────────────────────────────────────
# ── Market data ───────────────────────────────────────────────────────────────

class StrategyPrice(Base):
    """Serie storica giornaliera del valore (NAV) di ogni strategia."""
    __tablename__ = "strategy_prices"
    __table_args__ = (UniqueConstraint("strategy_id", "date"),)
 
    id          = Column(Integer, primary_key=True, autoincrement=True)
    strategy_id = Column(String, nullable=False, index=True)  # es. "ITMom10"
    date        = Column(Date,   nullable=False, index=True)
    value       = Column(Float,  nullable=False)
    currency    = Column(String, default="EUR")

class BenchmarkPrice(Base):
    """
    Serie storica di ogni indice benchmark.
    Ogni indice esiste una sola volta — nessuna duplicazione per strategia.
    Le associazioni strategia↔benchmark sono in StrategyBenchmark.
    """
    __tablename__ = "benchmark_prices"
    __table_args__ = (UniqueConstraint("benchmark_ticker", "date"),)
 
    id               = Column(Integer, primary_key=True, autoincrement=True)
    benchmark_ticker = Column(String, nullable=False, index=True)  # es. "^GSPC"
    name             = Column(String)                              # es. "S&P 500"
    date             = Column(Date,   nullable=False, index=True)
    close            = Column(Float,  nullable=False)

class StrategyBenchmark(Base):
    """
    Tabella di giunzione many-to-many tra strategie e benchmark.
    Permette a più strategie di condividere lo stesso indice senza duplicare
    le serie storiche. Il campo label distingue benchmark primario/secondario.
    """
    __tablename__ = "strategy_benchmarks"
    __table_args__ = (UniqueConstraint("strategy_id", "benchmark_ticker"),)
 
    id               = Column(Integer, primary_key=True, autoincrement=True)
    strategy_id      = Column(String, nullable=False, index=True)
    benchmark_ticker = Column(String, nullable=False, index=True)
    
class StrategyHolding(Base):
    """
    Composizione di ogni strategia nel tempo (Slowly Changing Dimension Type 2).
    Ogni ribilanciamento chiude i record correnti (valid_to = data ribilanciamento)
    e apre nuovi record (valid_from = data ribilanciamento, valid_to = None).
    valid_to = None indica la composizione attualmente in vigore.
    """
    __tablename__ = "strategy_holdings"
    __table_args__ = (UniqueConstraint("strategy_id", "ticker", "valid_from"),)
 
    id             = Column(Integer, primary_key=True, autoincrement=True)
    strategy_id    = Column(String, nullable=False, index=True)
    ticker         = Column(String, nullable=False)
    name           = Column(String)                 # nome leggibile, es. "Stellantis NV"
    weight         = Column(Float)                  # peso percentuale nel portafoglio
    valid_from     = Column(Date,   nullable=False) # inizio validità composizione
    valid_to       = Column(Date,   nullable=True)  # fine validità; NULL = attuale
    BuyPrice       = Column(Float,   nullable=False)# 
    SellPrice      = Column(Float,   nullable=True) # 
    
