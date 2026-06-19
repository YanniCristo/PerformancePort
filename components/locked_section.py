from dash import html
import dash_bootstrap_components as dbc

def locked_section(content, required_tier="pro", section_id=None):
    """
    Wrappa qualsiasi contenuto Dash con un overlay di blocco.
    Il lock viene mostrato/nascosto via callback in base a user-tier.
    required_tier: "registered" | "pro"
    """
    
    lock_id = section_id or f"lock-overlay-{required_tier}"
    content_id = f"{lock_id}-content"   # ← id sul contenuto
    
    return html.Div([
        # Contenuto reale (sempre nel DOM, nascosto dal overlay)
        html.Div(content, id=content_id, className="locked-content-inner"),
        
        # Overlay lucchetto (visibile o nascosto via callback)
        html.Div([
            html.Div([
                html.Span("🔒", style={"fontSize": "48px"}),
                html.H4("Contenuto Premium"),
                html.P("Abbonati per sbloccare i Top Picks"),
                dbc.Button("Scopri i piani →", id="upgrade-from-lock-btn",
                           color="primary", className="mt-2"),
            ], className="lock-overlay-inner")
        ], id=lock_id, className="lock-overlay"),

    ], className="lockable-section")
