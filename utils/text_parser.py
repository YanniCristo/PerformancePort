import re
from dash import html

def parse_rich_text(text: str) -> list:
    """
    Parsa una stringa con sintassi markdown-like e restituisce
    una lista di componenti Dash (html.Span, html.B, dcc.Link, ecc.)
    
    Supporta:
      **testo**     → html.B (grassetto)
      *testo*       → html.Em (corsivo)
      [label](/url) → html.A o dcc.Link (link interno)
    """
    from dash import dcc

    # Pattern unificato: ordine importante (** prima di *)
    pattern = r'(\*\*.*?\*\*|\*.*?\*|\[.*?\]\(.*?\))'
    parts = re.split(pattern, text)
    
    components = []
    for part in parts:
        if not part:
            continue

        # **grassetto**
        if re.fullmatch(r'\*\*.*?\*\*', part):
            inner = part[2:-2]
            components.append(html.B(inner))

        # *corsivo*
        elif re.fullmatch(r'\*.*?\*', part):
            inner = part[1:-1]
            components.append(html.Em(inner))

        # [label](/url) → link interno con dcc.Link
        elif re.fullmatch(r'\[.*?\]\(.*?\)', part):
            match = re.match(r'\[(.*?)\]\((.*?)\)', part)
            label, url = match.group(1), match.group(2)
            # Link interno Dash (usa dcc.Link per navigazione SPA)
            if url.startswith('/'):
                components.append(
                    dcc.Link(label, href=url, className="card-link")
                )
            # Link esterno
            else:
                components.append(
                    html.A(label, href=url, target="_blank", className="card-link")
                )
        # Testo semplice
        else:
            components.append(html.Span(part))

    return components
