from dash import html

def holdings_table(holdings: list[dict]) -> html.Div:
    # Costruisce la tabella HTML delle holding.
    
    if not holdings:
        return html.Div("Nessun dato disponibile.", className="holdings-empty")
 
    header = html.Div([
        html.Span("ISIN",   className="holdings-col col-ticker"),
        html.Span("Asset",     className="holdings-col col-name"),
        html.Span("Prezzo",   className="holdings-col col-price"),
    ], className="holdings-row holdings-header")
 
    rows = [header]
    for h in holdings:
        price = f"{h['buy_price']:.2f}" if h['buy_price'] is not None else "—"
        rows.append(html.Div([
            html.Span(h["ticker"], className="holdings-col col-ticker"),
            html.Span(h["name"],   className="holdings-col col-name"),
            html.Span(price,       className="holdings-col col-price"),
        ], className="holdings-row"))
 
    return html.Div(rows, className="holdings-table")
