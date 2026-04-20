from dash import Input, Output
import importlib

from db.database import get_payment_by_id
from payments.stripe_service import retrieve_checkout_session
import stripe

PAGE_REGISTRY = {
    "/indinvest":   ("layouts.indinvest_layout",  "indinvest_layout"),
    "/timehor":     ("layouts.timehoriz_layout",  "timehoriz_layout"),
    "/market":      ("layouts.market_layout",     "market_layout"),
    "/FAQ":         ("layouts.FAQ",               "FAQ_layout"),
    "/equitystrat": ("layouts.equity_strategy",   "equity_strategy"),
    "/marketphase": ("layouts.marketphase",       "marketphase"),
    "/macroall":    ("layouts.macroallocation",   "macroallocation"),
    "/ecoview":     ("layouts.eco_view",          "eco_view"),
    "/contact":     ("layouts.contact_layout",    "contact_layout"),
}
 
def _load_layout(path: str, lang: str):
    """Carica dinamicamente la funzione di layout dalla registry."""
    module_path, func_name = PAGE_REGISTRY[path]
    module = importlib.import_module(module_path)
    return getattr(module, func_name)(lang=lang)

def register(app):
    @app.callback(
        Output("page-content", "children"),
        Input("url", "pathname"),
        Input("url", "search"),
        Input("lang-store", "data"),
    )
    def display_page(pathname, search, lang):
        path = pathname.rstrip("/") or "/"
        
        if path in PAGE_REGISTRY:
            return _load_layout(path, lang)

        elif path == "/pagamento-completato":
            # Estrai session_id dalla query string (?session_id=cs_xxx)
            session_id = ""
            if search:
                for part in search.lstrip("?").split("&"):
                    if part.startswith("session_id="):
                        session_id = part.split("=", 1)[1]
                        break

            # Caso 1: webhook già arrivato → DB è la fonte di verità
            if session_id:
                payment = get_payment_by_id(session_id)
                if payment:
                    return success_layout(payment=payment, lang=lang)

            # Caso 2: webhook non ancora arrivato → fallback Stripe API
            if session_id:
                try:
                    session = retrieve_checkout_session(session_id)
                    return success_layout(session=session, lang=lang)
                except stripe.error.StripeError:
                    pass

            # Caso 3: session_id mancante o errore
            return success_layout(lang=lang)
        
        else:
            from layouts.home_layout import home_layout
            return home_layout(lang=lang)
