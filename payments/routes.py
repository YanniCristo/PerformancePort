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
    lang = request.args.get("lang", "en")

    if not session_id:
        logger.warning("Redirect /success senza session_id")
        return redirect(f"/{lang}/pagamento-completato")

    # Redirect alla pagina Dash passando il session_id come query param
    return redirect(f"/{lang}/pagamento-completato?session_id={session_id}")


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
