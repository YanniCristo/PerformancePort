from db.database import engine
import pandas as pd
from sqlalchemy import text

with engine.connect() as conn:
    row = conn.execute(text("SELECT MIN(date), MAX(date) FROM strategy_prices")).fetchone()

class data:
    index = type('obj', (object,), {
        'min': lambda self: pd.to_datetime(row[0]),
        'max': lambda self: pd.to_datetime(row[1]),
    })()
