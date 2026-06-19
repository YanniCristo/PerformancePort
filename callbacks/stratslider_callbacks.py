import dash
from dash import Input, Output, State, ALL, ctx, html
from utils.functions import load_content
from db.query import get_rebalancing_dates, get_holdings_at_date
from components.strat_holding import holdings_table
from flask_login import current_user

cards_DICT = load_content('assets/contents/equitystrategy/Strategies.json')
cards = list(cards_DICT.values())
        
CARD_WIDTH = 240
GAP = 12

# Dati placeholder per utenti non autorizzati
PLACEHOLDER_HOLDINGS = [
    {"ticker": f"Ticker{i}", "name":"Asset{i}", "buy_price": 100.0, "weight": round(10.0, 1)}
    for i in range(1, 11)]

def register(app):

    ############################################################################
    # Click sulle frecce → scorre le strategie
    @app.callback(
        Output("slider-index", "data"),
        Output("prev-btn", "disabled"),
        Output("next-btn", "disabled"),
        Input("prev-btn", "n_clicks"),
        Input("next-btn", "n_clicks"),
        State("slider-index", "data"),
        prevent_initial_call=True
    )
    def navigate(prev, next_, idx):
        ctx = dash.callback_context.triggered_id
        max_idx = len(cards) - 1
        if ctx == "prev-btn":
            idx = max(0, idx - 1)
        elif ctx == "next-btn":
            idx = min(max_idx, idx + 1)
        return idx, idx == 0, idx >= max_idx

    app.clientside_callback(
        """
        function(idx) {
            var STEP = 240 + 12;
            var track = document.getElementById('cards-track');
            if (track) {
                track.style.transform = 'translateX(-' + (idx * STEP) + 'px)';
            }
            return window.dash_clientside.no_update;
        }
        """,
        Output("slider-dummy", "data"),
        Input("slider-index", "data"),
        prevent_initial_call=True
    )


    ############################################################################
    # Click sulla card → aggiorna selected-strategy e classi CSS
    @app.callback(
        Output("selected-strategy", "data"),
        Output({"type": "strategy-card", "index": ALL}, "className"),
        Output("strat-description-content", "children"),
        Output("holdings-date-index", "data"),                          # reset all'ultima composizione
        Input({"type": "strategy-card", "index": ALL}, "n_clicks"),
        State("lang-store", "data"),
        prevent_initial_call=True
    )
    def select_card(n_clicks_list, lang):
        triggered = ctx.triggered_id
        if not triggered:
            raise dash.exceptions.PreventUpdate

        CARDS_DICT = load_content('assets/contents/equitystrategy/Strategies.json', lang=lang)
        CARDS_KEYS = list(CARDS_DICT.keys())

        selected_key = triggered["index"]
        card_data = CARDS_DICT[selected_key]

        classes = [
            "slider-card selected-card" if k == selected_key else "slider-card"
            for k in CARDS_KEYS
        ]

        description = card_data.get("desc", "-")
        strategy = card_data.get("tag", "-")
        
        return strategy, classes, description, 0


    ############################################################################
    # Frecce navigazione composizioni → aggiorna indice data
    @app.callback(
        Output("holdings-date-index", "data", allow_duplicate=True),
        Input("holdings-prev-btn", "n_clicks"),
        Input("holdings-next-btn", "n_clicks"),
        State("holdings-date-index", "data"),
        State("selected-strategy", "data"),
        prevent_initial_call=True
    )
    def navigate_holdings(prev_clicks, next_clicks, current_idx, strategy_tag):
        triggered_id = ctx.triggered_id
        
        dates = get_rebalancing_dates(strategy_tag)
        if not dates:
            raise dash.exceptions.PreventUpdate
 
        max_idx = len(dates) - 1
        if triggered_id == "holdings-prev-btn":
            new_idx = min(current_idx + 1, max_idx)   # +1 = più indietro nel tempo
        else:
            new_idx = max(current_idx - 1, 0)          # -1 = più recente
        return new_idx


    ############################################################################
    # Aggiornamento tabella composizione al cambio di strategia o di indice data
    @app.callback(
        Output("selection-row", "children"),
        Output("holdings-date-label", "children"),
        Output("holdings-prev-btn", "disabled"),
        Output("holdings-next-btn", "disabled"),
        Input("selected-strategy", "data"),
        Input("holdings-date-index", "data"),
        State("user-tier", "data")
    )
    def update_holdings(strategy_tag, date_idx, user_tier):

        # ── GUARDIA SICUREZZA ──────────────────────────────────────────
        if not current_user.is_authenticated or not current_user.is_paid:
            table = holdings_table(PLACEHOLDER_HOLDINGS)
            return (table, "-", True, True)   # dati finti, frecce disabilitate
        
        dates = get_rebalancing_dates(strategy_tag)

        if not dates:
            return (html.Div("-", className="holdings-empty"),
                    "—", True, True)
 
        date_idx = min(date_idx or 0, len(dates) - 1)
        selected_date = dates[date_idx]
        holdings = get_holdings_at_date(strategy_tag, selected_date)
 
        table = holdings_table(holdings)
 
        # Etichetta data formattata (es. "Feb 2026")
        from datetime import date as dt_type
        import datetime
        d = datetime.date.fromisoformat(selected_date)
        label = d.strftime("%b %Y")
 
        prev_disabled = date_idx >= len(dates) - 1   # già alla più vecchia
        next_disabled = date_idx <= 0                 # già alla più recente
 
        return table, label, prev_disabled, next_disabled
