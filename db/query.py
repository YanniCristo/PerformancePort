from db.database import engine
from sqlalchemy import text
from datetime import datetime
import pandas as pd

def get_strategy(strategy_id: str, start_date, end_date) -> pd.DataFrame:
   # Restituisce un df con la strategia selezionata e il suo bmk

        start_str = pd.to_datetime(start_date).strftime("%Y-%m-%d")
        end_str = pd.to_datetime(end_date).strftime("%Y-%m-%d")
    
        # Prende i benchmark associati alla strategia
        with engine.connect() as conn:
                benchmarks = conn.execute(text(
                    "SELECT benchmark_ticker FROM strategy_benchmarks WHERE strategy_id = :s"
                ), {"s": strategy_id}).fetchall()

        benchmark_tickers = [r[0] for r in benchmarks]

        # Serie storica della strategia
        df_strategy = pd.read_sql(
                        """SELECT date, value FROM strategy_prices WHERE strategy_id = :s
                        AND date >= :start_date AND date < :end_date ORDER BY date""",
                engine, params={"s": strategy_id,
                                "start_date": start_str,
                                "end_date": end_str}, index_col="date", parse_dates=["date"]
        )
        df_strategy.columns = [strategy_id]

        # Serie storiche dei benchmark
        for ticker in benchmark_tickers:
                df_bmk = pd.read_sql(
                    """SELECT date, close FROM benchmark_prices WHERE benchmark_ticker = :t
                        AND date >= :start_date AND date < :end_date ORDER BY date""",
                    engine, params={"t": ticker,
                                    "start_date": start_str,
                                    "end_date": end_str}, index_col="date", parse_dates=["date"]
                )
                df_bmk.columns = [ticker]
                df_strategy = df_strategy.join(df_bmk, how="left")

        return df_strategy


def get_rebalancing_dates(strategy_id: str) -> list:
   # Restituisce la lista di date di ribilanciamento, dalla più recente alla più vecchia.
   with engine.connect() as conn:
      dates = conn.execute(text(
         "SELECT DISTINCT valid_from FROM strategy_holdings WHERE strategy_id = :s ORDER BY valid_from DESC"
      ), {"s": strategy_id}).fetchall()
   return [str(r[0]) for r in dates]


def get_holdings_at_date(strategy_id: str, date: str) -> list[dict]:
    # Restituisce i titoli in portafoglio per una specifica data di ribilanciamento.

    with engine.connect() as conn:
        rows = conn.execute(text(
            """SELECT ticker, name, weight, BuyPrice, SellPrice FROM strategy_holdings
               WHERE strategy_id = :s AND valid_from = :d ORDER BY weight DESC"""
        ), {"s": strategy_id, "d": date}).fetchall()
        
    return [{
               "ticker":     r[0],
               "name":       r[1],
               "weight":     r[2],
               "buy_price":  r[3],
               "sell_price": r[4],
            } for r in rows]
