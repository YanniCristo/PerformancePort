from db.database import engine
from sqlalchemy import text
from datetime import datetime
import pandas as pd

def get_rebalancing_dates(strategy_id: str) -> list:
   # Restituisce la lista di date di ribilanciamento, dalla più recente alla più vecchia.
   with engine.connect() as conn:
      dates = conn.execute(text(
         """SELECT DISTINCT valid_from FROM strategy_holdings
            WHERE strategy_id = :s ORDER BY valid_from DESC"""
      ), {"s": strategy_id}).fetchall()
   return [str(r[0]) for r in dates]


def get_holdings_at_date(strategy_id: str, date: str) -> list[dict]:
    # Restituisce i titoli in portafoglio per una specifica data di ribilanciamento.

    with engine.connect() as conn:
        rows = conn.execute(text(
            """SELECT ticker, name, weight, "BuyPrice", "SellPrice" FROM strategy_holdings
               WHERE strategy_id = :s AND valid_from = :d ORDER BY weight DESC"""
        ), {"s": strategy_id, "d": date}).fetchall()
        
    return [{
               "ticker":     r[0],
               "name":       r[1],
               "weight":     r[2],
               "buy_price":  r[3],
               "sell_price": r[4],
            } for r in rows]
