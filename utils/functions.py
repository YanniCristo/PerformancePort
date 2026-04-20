import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException

from datetime import datetime
from dash import html
import json
import os

def load_content(path, lang="en"):
    localized = path.replace(".json", f".{lang}.json")
    with open(localized) as f:
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
