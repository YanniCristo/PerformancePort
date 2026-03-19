from dash import Input, Output
import plotly.express as px
from utils.data import data


def chart_callbacks(app):

    @app.callback(
        Output('graph', 'figure'),
        Input('date-picker', 'start_date'),
        Input('date-picker', 'end_date'),
        Input('ticker-dropdown', 'value')
    )
    def update_graph(start_date, end_date, ticker):
        
        # Filtra i dati per l'intervallo selezionato
        filtered = data.loc[start_date:end_date, ticker]

        # Calcola il rendimento cumulativo a partire dalla prima data selezionata
        returns = filtered.pct_change().fillna(0)  # rendimenti giornalieri
        cumulative = (1 + returns).cumprod()      # cumulativo a partire da start_date

        # Crea il grafico
        fig = px.line(x=filtered.index, y=cumulative, title=f"Serie storica {ticker}")
        return fig
