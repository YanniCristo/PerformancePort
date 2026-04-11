import dash_bootstrap_components as dbc
from dash import html


def success_layout(payment=None, session=None):
    """
    Layout della pagina di successo post-pagamento.

    Parametri (opzionali, passati da routes.py):
    - payment : dict dal DB  (priorità 1 — webhook già arrivato)
    - session : oggetto Stripe (priorità 2 — fallback API)
    """

    # ── Determina stato e dati da mostrare ────────────────────────────────────

    is_sub     = False
    is_pending = False
    amount_str = None
    email_str  = None
    session_id = None

    if payment:
        session_id = payment.get("id", "")
        status     = payment.get("status", "")
        is_pending = status != "paid"

        if not is_pending:
            raw = payment.get("amount")
            amount_str = f"{raw / 100:.2f} €" if raw else None
            email_str  = payment.get("email")

    elif session:
        session_id = getattr(session, "id", "")
        is_sub     = getattr(session, "mode", None) == "subscription"
        is_pending = getattr(session, "payment_status", "") != "paid" and not is_sub

    # ── Varianti testuali ─────────────────────────────────────────────────────

    if is_pending:
        icon      = "⏳"
        badge_txt = "In elaborazione"
        badge_cls = "badge-pending"
        title     = "Pagamento in attesa"
        subtitle  = (
            "Il tuo pagamento è in corso di verifica. "
            "Riceverai una conferma via email non appena sarà completato.")

    elif is_sub:
        icon      = "♾️"
        badge_txt = "Abbonamento attivato"
        badge_cls = "badge-sub"
        title     = "Abbonamento attivato!"
        subtitle  = (
            "Benvenuto! Il tuo abbonamento è ora attivo. "
            "Riceverai tutti i dettagli via email a breve.")

    else:
        icon      = "✓"
        badge_txt = "Pagamento completato"
        badge_cls = "badge-success"
        title     = "Grazie per il tuo acquisto!"
        subtitle  = (
            "Il pagamento è stato elaborato con successo. "
            "Riceverai una ricevuta via email a breve.")

    # ── Riga dettagli (solo per pagamento riuscito) ───────────────────────────

    detail_row = None
    if not is_pending and not is_sub:
        items = []
        if amount_str:
            items.append(
                html.Span([html.Strong("Importo: "), amount_str], className="detail-item")
            )
        if email_str:
            items.append(
                html.Span([html.Strong("Email: "), email_str], className="detail-item")
            )
        if session_id:
            short_id = session_id[:28] + "…" if len(session_id) > 28 else session_id
            items.append(
                html.Span([html.Strong("ID: "), short_id], className="detail-item detail-id")
            )
        if items:
            detail_row = html.Div(items, className="detail-box")

    # ── Layout ────────────────────────────────────────────────────────────────

    return html.Div([

        dbc.Container([
            dbc.Row(
                dbc.Col(

                    dbc.Card([
                        dbc.CardBody([

                            # Icona
                            html.Div(icon, className=f"success-icon {badge_cls}-icon"),

                            # Badge
                            html.Span(badge_txt, className=f"success-badge {badge_cls}"),

                            # Titolo
                            html.H2(title, className="success-title"),

                            # Sottotitolo
                            html.P(subtitle, className="success-subtitle"),

                            # Dettagli (solo pagamento one-time)
                            detail_row or html.Div(),

                            html.Hr(className="success-divider"),

                            # Bottone home
                            dbc.Button([
                                html.I(className="bi bi-house-fill me-2"),
                                "Torna alla homepage"
                            ],
                                href="/",
                                color="dark",
                                className="success-btn",
                                external_link=True
                            ),

                        ])
                    ], className="success-card"),

                    width={"size": 8, "offset": 3},
                    lg={"size": 7, "offset": 4},
                )
            )
        ], fluid=False),

    ], className=f"success-page {'success-page--pending' if is_pending else 'success-page--sub' if is_sub else 'success-page--paid'}")
