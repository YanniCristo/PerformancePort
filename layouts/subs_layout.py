from dash import html, dcc
from utils.functions import load_content
 
 
def subscriptions_layout(lang='en'):
    txt = load_content("assets/contents/subscriptions/texts.json", lang)

    header = txt.get("header", {})
    plans = txt.get("plans", [])

    return html.Div([
 
        # Header sezione
        html.Div([
            html.P(header.get("subtitle"), className="subs-subtitle"),
            html.H1(header.get("title"), className="subs-title"),
            html.P(header.get("description"), className="subs-description"),
        ], className="subs-header"),
 
        # Cards piani
        html.Div([_plan_card(plan)
                  for plan in plans
        ], className="subs-cards-wrapper"),
 
        html.Div(style={"minHeight": "10vh"}),
 
    ], className="subs-content")

def _plan_card(plan):
    card_class = "subs-card"
    if plan.get("highlighted"):
        card_class += " subs-card--highlighted"
 
    gradient_class = f"subs-card-gradient subs-card-gradient--{plan.get('id', 'basic')}"
 
    features = [
        html.Li([
            html.Span("✓", className="subs-feature-check"),
            feature
        ], className="subs-feature-item")
        for feature in plan.get("features", [])
    ]
 
    return html.Div([
 
        # Badge "Most Popular" solo per il piano highlighted
        html.Div("Most Popular", className="subs-badge") if plan.get("highlighted") else html.Div(),
 
        # Nome piano
        html.H2(plan.get("name", ""), className="subs-plan-name"),
 
        # Area gradiente con features
        html.Div([
            html.Ul(features, className="subs-features-list"),
        ], className=gradient_class),
 
        # Prezzo
        html.Div([
            html.Span("$", className="subs-currency"),
            html.Span(plan.get("price", "0"), className="subs-price-amount"),
            html.Span(f".{plan.get('cents', '00')}", className="subs-price-cents"),
            html.Div(plan.get("period", "per month"), className="subs-period"),
        ], className="subs-price-wrapper"),
 
        # CTA
        html.Button(
            plan.get("cta", "Buy"),
            id=plan.get("buttID", ""), #id={"type": "subs-cta-btn", "plan": plan.get("id", "")},
            n_clicks=0,
            className="subs-cta-btn",
        ),
 
    ], className=card_class)
