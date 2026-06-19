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
        <p>Thanks for your registration.</p>
        <p>Click the button to verify your account:</p>
        <a href="{verify_link}">Click Here</a>
        """
    )

    try:
        api_response = api_instance.send_transac_email(send_smtp_email)
    except ApiException as e:
        print(f"Errore durante l'invio tramite Brevo: {e}")

def send_reset_password_email_Brevo(to_email: str, token: str):
    """Invia all'utente un link per reimpostare la password via Brevo."""
 
    configuration = sib_api_v3_sdk.Configuration()
    configuration.api_key['api-key'] = os.getenv("BREVO_API_KEY")
 
    api_instance = sib_api_v3_sdk.TransactionalEmailsApi(
        sib_api_v3_sdk.ApiClient(configuration))
 
    BASE_URL = os.getenv("BASE_URL", "http://127.0.0.1:8015")
    reset_link = f"{BASE_URL}/reset-password?token={token}"
 
    sender = {"name": "PerformingPort", "email": "riera89@hotmail.it"}
    to     = [{"email": to_email}]
 
    send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(
        to=to,
        sender=sender,
        subject="Reset your password – PerformingPort",
        html_content=f"""
        <p>Hi,</p>
        <p>We received a request to reset the password for your account.</p>
        <p>Click the button below to choose a new password. This link is valid for <strong>1 hour</strong>.</p>
        <p style="margin: 24px 0;">
            <a href="{reset_link}"
               style="background:#4a90d9;color:#fff;padding:12px 24px;
                      border-radius:6px;text-decoration:none;font-weight:bold;">
                Reset password
            </a>
        </p>
        <p>If you did not request a password reset, you can safely ignore this email.</p>
        <p style="color:#888;font-size:12px;">
            Or copy this link into your browser:<br>{reset_link}
        </p>
        """
    )
 
    try:
        api_instance.send_transac_email(send_smtp_email)
    except ApiException as e:
        print(f"Errore invio reset email via Brevo: {e}")

def send_subscription_confirmation_email_Brevo(to_email: str):
    """Invia all'utente una mail di conferma dopo che il pagamento premium è andato a buon fine."""
 
    configuration = sib_api_v3_sdk.Configuration()
    configuration.api_key['api-key'] = os.getenv("BREVO_API_KEY")
 
    api_instance = sib_api_v3_sdk.TransactionalEmailsApi(
        sib_api_v3_sdk.ApiClient(configuration))
 
    BASE_URL = os.getenv("BASE_URL", "http://127.0.0.1:8015")
 
    sender = {"name": "PerformingPort", "email": "riera89@hotmail.it"}
    to     = [{"email": to_email}]

    print(to_email)
 
    send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(
        to=to,
        sender=sender,
        subject="Welcome to PerformingPort Premium! 🎉",
        html_content=f"""
        <p>Hi,</p>
        <p>Your Premium subscription has been activated successfully. You now have full access to all PerformingPort features.</p>
        <p style="margin: 24px 0;">
            <a href="{BASE_URL}"
               style="background:#4a90d9;color:#fff;padding:12px 24px;
                      border-radius:6px;text-decoration:none;font-weight:bold;">
                Go to PerformingPort
            </a>
        </p>
        <p>Thank you for subscribing. If you have any questions, feel free to reach out.</p>
        <p style="color:#888;font-size:12px;">
            The PerformingPort Team
        </p>
        """
    )
 
    try:
        api_instance.send_transac_email(send_smtp_email)
    except ApiException as e:
        print(f"Errore invio subscription confirmation email via Brevo: {e}")

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

def get_macros() -> pd.DataFrame:
        
        with engine.connect() as conn:
                result = conn.execute(text("SELECT macro_id, macro_name, date, value FROM eco_macro ORDER BY date"))        
                df_long = pd.DataFrame(result.fetchall())

        # Pivot: righe = date, colonne = macro_id
        df_wide = df_long.pivot(index="date", columns="macro_id", values="value")

        # Lista dei nomi delle variabili e indice associato
        df_names = df_long.drop_duplicates("macro_id").set_index("macro_id")["macro_name"]

        return df_wide, df_names
        
