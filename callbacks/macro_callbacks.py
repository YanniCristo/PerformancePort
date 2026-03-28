from utils.functions import load_content, load_image, q_to_dt
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
from dash import Input, Output
from dash import html, dcc
from pathlib import Path
import pandas as pd
import dash

def AddChart(df, idx, nome):
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df.index, y=df[idx],
        mode='lines'))
    
    fig.update_layout(
        margin=dict(l=25, r=25, t=25, b=25),
        height=250,
        xaxis=dict(fixedrange=True), yaxis=dict(fixedrange=True, side='right'),
        font=dict(color="white"), paper_bgcolor="rgba(116, 159, 219, 0.2)",
        #plot_bgcolor="rgba(116, 159, 219, 0.68)")

        title=dict(
            text=nome,
            x=0.5,  # centro
            xanchor='center',
            yanchor='top',
            font=dict(size=12, color='white')
            )
        )
    

    return dcc.Graph(figure=fig, config={"displayModeBar": False})

def register(app):

    @app.callback(
        Output('artic-ecoview', 'children'),
        Input('quarter-dd', 'value')
    )
    def update_article(q):
        data = load_content(f'assets/contents/ecoview/articles/{q}/text.json')
        base_path = Path(f'assets/contents/ecoview/articles/{q}')
        df = pd.read_excel(f'assets/contents/ecoview/articles/EcoData.xlsx', header=0, index_col=0)

        names = df.iloc[0,:]
        df.drop('Nome Grafico', inplace=True)
        end = pd.to_datetime(q_to_dt(q))
        df = df[df.index <= end]
        
        content = []

        for i, key in enumerate(data):
            par = data[key]

            title = par.get("title", "")
            imgs = par.get("img", [])
            desc = par.get("description", "")

            row = []

            # Titolo (se presente)
            if title:
                row.append(html.H3(title, className="article-title"))

            # Se grafico
            if imgs:
                row.append(
                    html.Div([
                        
                        dbc.Card(
                            dbc.CardBody(
                                html.P(desc, style={"whiteSpace": "pre-line"})
                                ), className="article-column article-card"),
                        
                        html.Div(
                            [AddChart(df, img, names[img]) for img in imgs],
                            className="article-column")
                        
                    ], className=f"article-row {'reverse' if i % 2 else ''}")
                )
                
            else:
            # Altrimenti solo testo
                row.append(html.P(desc, style={"whiteSpace": "pre-line"},
                                  className="article-rowtext"))

            content.append(html.Div(row, className="article-block"))

        return content
