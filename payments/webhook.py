from db.database import save_payment, event_exists, save_event, save_subscription, update_user_to_paid_by_id, set_stripe_customer_id, update_user_to_paid_by_stripe_customer
import logging, os, stripe
from utils.functions import send_subscription_confirmation_email_Brevo

logger = logging.getLogger(__name__)

def handle_webhook(request):

    # Chave per verificare che la chiamata venga da Stripe
    endpoint_secret = os.getenv("STRIPE_WEBHOOK_SECRET")
    payload = request.data
    sig_header = request.headers.get("Stripe-Signature")

    # Controlla validità di firma e secret_endpoint
    try:
        event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
    except ValueError:
        logger.error("Webhook: payload non valido")
        return "Payload non valido", 400
    except stripe.error.SignatureVerificationError:
        logger.error("Webhook: firma non valida")
        return "Firma non valida", 400
    
    event_id = event["id"]
    event_type = event["type"]

    # IDPOTENZA: evita doppia elaborazione
    if event_exists(event_id):
        logger.info(f"Evento già processato, skip: {event_id}")
        return "", 200

    logger.info(f"Nuovo evento ricevuto: {event_type} ({event_id})")

    # VERA CONFERMA TRANSAZIONE E REFRESH DB
    try:
        session = event["data"]["object"]

        print(event_type)

        # Evento principale
        if event_type == "checkout.session.completed":
            if session.mode == "payment":
                save_payment(session)
                if session.client_reference_id:
                    update_user_to_paid_by_id(int(session.client_reference_id))

                    #Invio Mail
                    try:
                        user_email = session.customer_details.email
                        if user_email:
                            send_subscription_confirmation_email_Brevo(user_email)
                            logger.info(f"Mail di conferma subscription inviata a {user_email}")
                        else:
                            logger.warning(f"invoice.paid: nessuna email trovata per customer {customer_id}")
                    except Exception as email_err:
                        logger.error(f"Errore invio mail conferma subscription: {email_err}")
                    
            elif session.mode == "subscription":
                if session.client_reference_id and session.customer:
                    set_stripe_customer_id(int(session.client_reference_id), session.customer)

        # Pagamenti asincroni (bonifici, ecc.)
        elif event_type in ("checkout.session.async_payment_succeeded",
                            "checkout.session.async_payment_failed"):
            save_payment(session)

        # Fallback più basso livello (extra sicurezza)
        elif event_type == "payment_intent.succeeded":
            logger.info(f"payment_intent.succeeded: {session.id}")

        # -- Abbonamenti
        elif event_type == "customer.subscription.created":
            save_subscription(session)

        elif event_type == "customer.subscription.updated":
            save_subscription(session)

        elif event_type == "customer.subscription.deleted":
            save_subscription(session)  # status sarà "canceled"

        elif event_type == "invoice.paid":
            
            # Rinnovo mensile riuscito
            customer_id = session.customer
            if customer_id:
                update_user_to_paid_by_stripe_customer(customer_id)

            # Invia mail di conferma subscription solo al primo pagamento andato a buon fine
            # billing_reason == "subscription_create" identifica il primo invoice (non i rinnovi)
            billing_reason = session.get("billing_reason", "")
            if billing_reason == "subscription_create":
                try:
                    customer = stripe.Customer.retrieve(customer_id)
                    user_email = customer.email
                    if user_email:
                        send_subscription_confirmation_email_Brevo(user_email)
                        logger.info(f"Mail di conferma subscription inviata a {user_email}")
                    else:
                        logger.warning(f"invoice.paid: nessuna email trovata per customer {customer_id}")
                except Exception as email_err:
                    logger.error(f"Errore invio mail conferma subscription: {email_err}")

            logger.info(f"Fattura pagata: {session.id}")

        elif event_type == "invoice.payment_failed":
            # Rinnovo fallito → notifica utente o sospendi accesso
            logger.warning(f"Fattura fallita: {session.id}")

        else:
            logger.debug(f"Evento non gestito: {event_type}")

        # Salva SEMPRE evento
        save_event(event_id, event_type)

    except Exception as e:
        logger.error(f"Errore processing evento {event_id}: {e}", exc_info=True)
        return "Errore interno", 500

    return "", 200
