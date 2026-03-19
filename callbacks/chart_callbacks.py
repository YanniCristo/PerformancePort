from dash import Input, Output
import plotly.express as px
from utils.data import data
from datetime import datetime, timedelta
import pandas as pd
import dash

def chart_callbacks(app):

    @app.callback(
        Output('graph', 'figure'),
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
            yaxis=dict(
                side="right",
                title="Cumulativo",
                ticks="outside",
                showline=True,
                mirror=True
            )
        )
        return fig, start, end

