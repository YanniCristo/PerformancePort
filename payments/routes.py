import logging
import stripe
from flask import Blueprint, request, jsonify, redirect
from payments.webhook import handle_webhook
from db.database import get_payment_by_id

logger = logging.getLogger(__name__)

payment_bp = Blueprint("payments", __name__)

# Stripe post pagamento o altro evento
@payment_bp.route("/webhook", methods=["POST"])
def stripe_webhook():
    return handle_webhook(request)


# Browser post redirect su '/success'
@payment_bp.route("/success")
def success():
    session_id = request.args.get("session_id")

    if not session_id:
        logger.warning("Redirect /success senza session_id")
        return redirect("/pagamento-completato")

    # Redirect alla pagina Dash passando il session_id come query param
    return redirect(f"/pagamento-completato?session_id={session_id}")



##    session_id = request.args.get("session_id")
##    if not session_id:
##        return "Pagamento completato, ma session_id mancante.", 400
##
##    # Caso 1: webhook già arrivato → DB aggiornato, fonte di verità
##    payment = get_payment_by_id(session_id)
##
##    if payment:
##        if payment["status"] == "paid":
##            return f"Pagamento riuscito! Sessione: {session_id}"
##        else:
##            # Record presente ma non pagato (es. async pending o failed)
##            return f"Pagamento non confermato. Stato: {payment['status']}", 202
##
##    # Caso 2: webhook non ancora arrivato → fallback su Stripe API
##    try:
##        session = retrieve_checkout_session(session_id)
##        if session.payment_status == "paid":
##            return f"Pagamento riuscito! Sessione: {session_id}"
##        else:
##            # Fix 1: non mostrare "completato" se non è effettivamente paid
##            return f"Pagamento non confermato. Stato: {payment['status']}", 202
##
##    except stripe.error.InvalidRequestError:
##        # Fix 2: session_id non valido o manomesso
##        logger.warning(f"session_id non valido ricevuto in /success: {session_id}")
##        return "Sessione non valida.", 400
##
##    except stripe.error.StripeError as e:
##        # Stripe irraggiungibile o altri errori API
##        logger.error(f"Errore Stripe in /success: {e}")
##        return "Pagamento completato, in attesa di conferma webhook.", 202


# Browser post redirect su '/cancel' - utente annulla pagamento
@payment_bp.route("/cancel")
def cancel():
    return "Pagamento annullato."


# Chiamato da frontend (no automatico)
# Serve per polling, debug, API interna
@payment_bp.route("/payment-status/<session_id>")
def payment_status(session_id):
    payment = get_payment_by_id(session_id)

    if not payment:
        return jsonify({
            "found": False,
            "paid": False,
            "status": "not_found",
        }), 404  # Fix 2: 404 è più corretto di 200 per "non trovato"

    return jsonify({
        "found": True,
        "paid": payment["status"] == "paid",
        "status": payment["status"],
        "payment": payment,
    })
