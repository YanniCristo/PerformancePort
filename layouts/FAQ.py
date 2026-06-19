import dash_bootstrap_components as dbc
from components.contact_form import contact_form
from dash import html, dcc
from utils.functions import load_content
import json

with open("assets/contents/FAQ/buttons.json", "r", encoding="utf-8") as f:
    but = json.load(f)
TOPICS = but["buttons"]
FIRST_TOPIC = TOPICS[0][0]  # id del primo topic, es. "PerformingPort"


# ── Helper: build the topic button row ───────────────────────────────────────
def _topic_buttons(active_id=None):
    buttons = []
    for btn_id, label, icon in TOPICS:
        is_active = btn_id == active_id
        buttons.append(
            html.Button(
                [html.Span(icon, style={"marginRight": "6px"}), label],
                id=btn_id,
                n_clicks=0,
                className="faq-topic-btn" + (" faq-topic-btn--active" if is_active else ""),
            )
        )
    return html.Div(buttons, id="faq-topic-row", className="faq-topic-row")


def FAQ_layout(lang='en'):
##    txt = load_content("assets/contents/FAQ/texts.json", lang)

    return html.Div([

        # ── Store per tracciare topic e domanda attivi ────────────────────────
        dcc.Store(id="faq-active-topic", data=FIRST_TOPIC),
        
        # ── Title ────────────────────────────────────────────────────────────
        html.H1("", className="FAQ-title"),

        # ── Row 1 – intro + topic buttons ────────────────────────────────────
        html.Div(
            _topic_buttons(active_id=FIRST_TOPIC), className="faq-row-1"
        ),

        # ── Row 2 – dynamic content area ─────────────────────────────────────
        html.Div(id="faq-content-area"),
        
    ], className="faq-wrapper")
