from dash import Input, Output
from layouts.home_layout import home_layout
from layouts.indinvest_layout import indinvest_layout
from layouts.timehoriz_layout import timehoriz_layout
from layouts.market_layout import market_layout
from layouts.equity_strategy import equity_strategy
from layouts.eco_view import eco_view
from layouts.contact_layout import contact_layout
from layouts.FAQ import FAQ_layout
from layouts.macroallocation import macroallocation
from layouts.marketphase import marketphase
from layouts.success import success_layout

from db.database import get_payment_by_id
from payments.stripe_service import retrieve_checkout_session
import stripe

def register(app):
    @app.callback(
        Output("page-content", "children"),
        Input("url", "pathname"),
        Input("url", "search")
    )
    def display_page(pathname, search):

        if pathname == "/indinvest":
            return indinvest_layout()

        elif pathname == "/timehor":
            return timehoriz_layout()

        elif pathname == "/market":
            return market_layout()

        elif pathname == "/FAQ":
            return FAQ_layout()

        elif pathname == "/equitystrat":
            return equity_strategy()

        elif pathname == "/marketphase":
            return marketphase()

        elif pathname == "/macroall":
            return macroallocation()
        
        elif pathname == "/ecoview":
            return eco_view()

        elif pathname == "/contact":
            return contact_layout()

        if pathname == "/pagamento-completato":
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
                    return success_layout(payment=payment)

            # Caso 2: webhook non ancora arrivato → fallback Stripe API
            if session_id:
                try:
                    session = retrieve_checkout_session(session_id)
                    return success_layout(session=session)
                except stripe.error.StripeError:
                    pass

            # Caso 3: session_id mancante o errore
            return success_layout()
        
        else:
            return home_layout()
