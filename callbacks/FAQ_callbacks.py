import dash_bootstrap_components as dbc
from utils.functions import load_content, hex_to_rgba, get_strategy
from utils.data import data
from dash import html
from dash import Input, Output, State, ctx, ALL, no_update
import plotly.express as px
from datetime import datetime, timedelta
import plotly.graph_objects as go
import pandas as pd
import dash
import json
import numpy as np


# ── Helper: content per topic ────────────────────────────────────────────────
with open("assets/contents/FAQ/buttons.json", "r", encoding="utf-8") as f:
    but = json.load(f)
TOPICS = but["buttons"]
btn_ids = [btn_id for btn_id, _, _ in TOPICS]
FIRST_TOPIC = btn_ids[0]


def _get_first_question_key(topic_id: str, txt: dict):
    """Restituisce la chiave della prima domanda del topic (es. 'Q_1'), o None."""
    content = txt.get(topic_id, {})
    for key in content:
        if key.startswith("Q_"):
            return key
    return None


def _get_answer(topic_id: str, q_key: str, txt: dict):
    """Restituisce il testo della risposta per la domanda q_key nel topic."""
    content = txt.get(topic_id, {})
    answer_key = "A_" + q_key[2:]
    return content.get(answer_key, "-")


def _topic_content(topic_id: str, txt: dict, active_question: str = None):
    """Costruisce il contenuto di row-2 per il topic selezionato."""
    content = txt.get(topic_id, {})

    questions = [
        html.Button(value,
                    id={"type": "faq-question", "index": key},
                    className="faq-question-btn" + (" faq-question-btn--active" if key == active_question else ""),
                    n_clicks=0)
        for key, value in content.items()
        if key.startswith("Q_")
    ]

    # Prepopola già la risposta se c'è una domanda attiva
    if active_question:
        answer_content = html.P(
            _get_answer(topic_id, active_question, txt),
            className="faq-answer-text"
        )
    else:
        answer_content = "Seleziona una domanda"

    return html.Div(
        [
            html.Div(questions, className="faq-questions-column"),
            html.Div(answer_content, id="faq-answer-container",
                     className="faq-answer-column"),
        ], className="faq-row-2"
    )


def register(app):

    # ── Callback 1: aggiorna lo Store del topic attivo ───────────────────────
    @app.callback(
        Output("faq-active-topic", "data"),
        [Input(btn_id, "n_clicks") for btn_id in btn_ids],
        prevent_initial_call=True,
    )
    def store_active_topic(*n_clicks_list):
        triggered_id = ctx.triggered_id
        if triggered_id is None:
            return no_update
        return triggered_id


    # ── Callback 2: evidenzia il topic button attivo ─────────────────────────
    @app.callback(
        [Output(btn_id, "className") for btn_id in btn_ids],
        Input("faq-active-topic", "data"),
    )
    def highlight_topic_button(active_topic):
        return [
            "faq-topic-btn faq-topic-btn--active" if btn_id == active_topic else "faq-topic-btn"
            for btn_id in btn_ids
        ]


    # ── Callback 3: costruisce il contenuto row-2 ────────────────────────────
    @app.callback(
        Output("faq-content-area", "children"),
        Input("faq-active-topic", "data"),
        Input("lang-store", "data"),
    )
    def update_content(active_topic, lang):
        if active_topic is None:
            return html.P("Seleziona un argomento per iniziare →", className="faq-placeholder")

        txt = load_content("assets/contents/FAQ/texts.json", lang)

        # Seleziona automaticamente la prima domanda del topic
        first_q = _get_first_question_key(active_topic, txt)
        return _topic_content(active_topic, txt, active_question=first_q)


    # ── Callback 4: mostra risposta ed evidenzia la domanda cliccata ─────────
    @app.callback(
        Output("faq-answer-container", "children"),
        Output({"type": "faq-question", "index": ALL}, "className"),
        Input({"type": "faq-question", "index": ALL}, "n_clicks"),
        State({"type": "faq-question", "index": ALL}, "id"),
        State("faq-active-topic", "data"),
        Input("lang-store", "data"),
        prevent_initial_call=True,
    )
    def update_answer(n_clicks_list, question_ids, active_topic, lang):
        triggered = ctx.triggered_id

        # Ignorato se non è stato premuto nessun bottone-domanda
        if triggered is None or not isinstance(triggered, dict):
            return no_update, no_update

        # Nessun click reale (callback fired solo per inizializzazione)
        if not any(n for n in n_clicks_list if n):
            return no_update, no_update

        # L'index del bottone premuto è "Q_1", "Q_2", ecc.
        active_q_key = triggered["index"]          # es. "Q_1"

        txt = load_content("assets/contents/FAQ/texts.json", lang)
        answer_text = _get_answer(active_topic, active_q_key, txt)

        answer_div = html.Div(
            html.P(answer_text, className="faq-answer-text")
        )

        new_classes = [
            "faq-question-btn faq-question-btn--active" if q_id["index"] == active_q_key
            else "faq-question-btn"
            for q_id in question_ids
        ]

        return answer_div, new_classes
