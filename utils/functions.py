import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException

from db.database import engine
from sqlalchemy import text
from datetime import datetime
from dash import html
import pandas as pd
import json
import os

def load_content(path, lang="en"):
    localized = path.replace(".json", f".{lang}.json")
    with open(localized, "r", encoding="utf-8") as f:
        return json.load(f)

def load_image(path, name='images'):
        return html.Img(src=path, className=name)

def q_to_dt(q_str: str) -> datetime:
    year_str, quarter_str = q_str.split('-Q')
    year = int(year_str)
    quarter = int(quarter_str)

    quarter_end = {
        1: (3, 31), 2: (6, 30),
        3: (9, 30), 4: (12, 31)}

    month, day = quarter_end[quarter]
    return datetime(year, month, day)

def hex_to_rgba(hex_color, alpha=0.1):
    hex_color = hex_color.lstrip("#")
    r, g, b = int(hex_color[0:2], 16), int(hex_color[2:4], 16), int(hex_color[4:6], 16)
    return f"rgba({r},{g},{b},{alpha})"

def send_verification_email_Brevo(to_email, token):
        
    # Configurazione API Key
    configuration = sib_api_v3_sdk.Configuration()
    configuration.api_key['api-key'] = os.getenv("BREVO_API_KEY")

    api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))

    BASE_URL = os.getenv("BASE_URL", "http://127.0.0.1:8015")
    verify_link = f"{BASE_URL}/verify?token={token}"

    # Definizione del mittente e del destinatario
    sender = {"name": "PerformingPort", "email": "riera89@hotmail.it"}
    to = [{"email": to_email}]
    
    # Creazione dell'oggetto email
    send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(
        to=to,
        sender=sender,
        subject="Verify your account",
        html_content=f"""
        <p>Thanks your registration.</p>
        <p>Click the button to verify your account:</p>
        <a href="{verify_link}">Click Here</a>
        """
    )

    try:
        api_response = api_instance.send_transac_email(send_smtp_email)
    except ApiException as e:
        print(f"Errore durante l'invio tramite Brevo: {e}")

def get_strategy(strategy_id: str, start_date, end_date) -> pd.DataFrame:
        start_str = pd.to_datetime(start_date).strftime("%Y-%m-%d")
        end_str = pd.to_datetime(end_date).strftime("%Y-%m-%d")

        params = {
                "s":          strategy_id,
                "start_date": start_str,
                "end_date":   end_str}
    
        # Prende i benchmark associati alla strategia
        with engine.connect() as conn:
                benchmarks = conn.execute(
                        text("SELECT benchmark_ticker FROM strategy_benchmarks WHERE strategy_id = :s"),
                        {"s": strategy_id}).fetchall()
        benchmark_tickers = [r[0] for r in benchmarks]

        # Serie storica della strategia
        with engine.connect() as conn:
                result = conn.execute(
                        text("""SELECT date, value FROM strategy_prices WHERE strategy_id = :s
                                  AND date >= :start_date
                                  AND date < :end_date
                                  ORDER BY date"""), params
                )
                df_strategy = pd.DataFrame(result.fetchall(), columns=["date", "value"])

        df_strategy["date"] = pd.to_datetime(df_strategy["date"])
        df_strategy = df_strategy.set_index("date")
        df_strategy.columns = [strategy_id]
    
        # Serie storiche dei benchmark
        for ticker in benchmark_tickers:
                with engine.connect() as conn:
                    result = conn.execute(
                        text("""SELECT date, close FROM benchmark_prices WHERE benchmark_ticker = :t
                                AND date >= :start_date
                                AND date < :end_date
                                ORDER BY date"""),
                        {"t": ticker, "start_date": start_str, "end_date": end_str}
                    )
                    df_bmk = pd.DataFrame(result.fetchall(), columns=["date", "close"])

                df_bmk["date"] = pd.to_datetime(df_bmk["date"])
                df_bmk = df_bmk.set_index("date")
                df_bmk.columns = [ticker]
                
                df_strategy = df_strategy.join(df_bmk, how="left")

        return df_strategy

