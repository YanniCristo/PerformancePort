import dash_bootstrap_components as dbc
from dash import html
from dash import Input, Output
import plotly.express as px
from utils.data import data
from datetime import datetime, timedelta
import pandas as pd
import dash
import numpy as np

def build_metrics(cumulative, returns):
    
    total_return = cumulative.iloc[-1] - 1
    volatility = returns.std() * np.sqrt(252)
    sharpe = (returns.mean() * 252) / volatility if volatility != 0 else 0
    rolling_max = cumulative.cummax()
    max_dd = ((cumulative - rolling_max) / rolling_max).min()
    calmar = (total_return / abs(max_dd)) if max_dd != 0 else 0

    metrics_data = [("Return", total_return, f"{total_return:.1%}"),
                    ("Sharpe Ratio", sharpe, f"{sharpe:.2f}"),
                    ("Volatility", volatility, f"{volatility:.1%}"),
                    ("Max Drawdown", max_dd, f"{max_dd:.1%}"),
                    ("Calmar Ratio", calmar, f"{calmar:.2f}")]
    cols = []
    for name, raw, value in metrics_data:
        if name in ['Return','Sharpe Ratio','Calmar Ratio']:
            if raw > 0: segno = "positive"
            elif raw < 0: segno = "negative"
        else:
            segno = "neutral"
        cols.append(
            dbc.Col(
                dbc.Card(
                    dbc.CardBody([
                        html.Div(name, className="metric-title"),
                        html.Div(value, className="metric-value", **{"data-sign": segno}),
                    ])
                ), xs=12, sm=6, md=4, lg=3, xl=2
            )
        )
    return dbc.Row(cols, className="metrics-row")

def register(app):

    @app.callback(
        Output('graph', 'figure'),
        Output('metrics-wrapper', 'children'),
        Output('date-picker', 'start_date'),
        Output('date-picker', 'end_date'),
        Input('date-picker', 'start_date'),
        Input('date-picker', 'end_date'),
        Input('ticker-dropdown', 'value'),
        Input("1Y-btn", "n_clicks"),
        Input("3Y-btn", "n_clicks"),
        Input("5Y-btn", "n_clicks"),
        Input("Max-btn", "n_clicks")
    )
    def update_graph(start_date, end_date, ticker,
                     one, three, five, max_):

        # default: usare date-picker
        start = pd.to_datetime(start_date)
        end = pd.to_datetime(end_date)

        # se un pulsante è stato premuto, sovrascrivi start/end
        ctx = dash.callback_context
        if ctx.triggered:
            btn_id = ctx.triggered[0]['prop_id'].split('.')[0]
            today = pd.to_datetime(data.index.max())
            if btn_id == "1Y-btn":
                start = today - pd.DateOffset(years=1)
                end = today
            elif btn_id == "3Y-btn":
                start = today - pd.DateOffset(years=3)
                end = today
            elif btn_id == "5Y-btn":
                start = today - pd.DateOffset(years=5)
                end = today
            elif btn_id == "Max-btn":
                start = data.index.min()
                end = today

        # Filtra i dati per l'intervallo selezionato
        filtered = data.loc[start:end, ticker]

        # Calcola il rendimento cumulativo a partire dalla prima data selezionata
        returns = filtered.pct_change().fillna(0)  # rendimenti giornalieri
        cumulative = (1 + returns).cumprod()      # cumulativo a partire da start_date

        # Crea il grafico
        fig = px.line(x=filtered.index, y=cumulative)
        
        fig.update_layout(

            yaxis=dict(side="right", title="",
                       ticks="outside",showline=False,
                       showgrid=True,mirror=True,
                       gridcolor="rgba(150,150,150,0.3)",
                       griddash="dot", zeroline=False
                       ),
            
            xaxis=dict(title=None, showline=False, showgrid=False),

            autosize=True,
            margin=dict(l=10, r=10, t=10, b=10),
            dragmode=False,
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            hovermode="x"
        )

        fig.update_xaxes(
            showspikes=True,          # attiva la linea verticale
            spikemode="across",       # attraversa tutto il grafico
            spikesnap="cursor",
            spikecolor="rgba(150,150,150,0.6)",
            spikethickness=1
        )

        # Calcolo le metriche
        metrics = build_metrics(cumulative, returns)
        
        return fig, metrics, start, end

