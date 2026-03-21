from utils.functions import load_content, load_image
from dash import Input, Output
from dash import html, dcc
from pathlib import Path
import dash

def macro_callbacks(app):

    @app.callback(
        Output('artic-ecoview', 'children'),
        Input('quarter-dd', 'value')
    )
    def update_article(q):
        data = load_content(f'assets/contents/ecoview/articles/{q}/text.json')
        base_path = Path(f'assets/contents/ecoview/articles/{q}')

        content = []

        for key in data:
            par = data[key]

            title = par.get("title", "")
            img = par.get("img", "")
            desc = par.get("description", "")

            row = []

            # Titolo (se presente)
            if title:
                row.append(html.H3(title, className="article-title"))

            # Se immagine
            if img:
                row.append(
                    html.Div([
                        html.Div(
                            html.P(desc, style={"whiteSpace": "pre-line"}),
                            className="article-column"
                        ),
                        html.Div(
                            html.Img(src=f"/{base_path}/{img}", style={"width": "100%"}),
                            className="article-column"
                        )
                    ], className="article-row")
                )
            else:
            # Altrimenti solo testo
                row.append(html.P(desc, style={"whiteSpace": "pre-line"},
                                  className="article-rowtext"))

            content.append(html.Div(row, className="article-block"))

        return content
