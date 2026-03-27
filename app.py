import os
from dash import Dash
import dash_bootstrap_components as dbc

from callbacks import register_all_callbacks
from layouts.main_layout import create_layout

app = Dash(__name__,
           title="PerformingPort.com",
           external_stylesheets=[dbc.themes.CYBORG])

server = app.server

register_all_callbacks(app)
app.layout = create_layout()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 9000))
    app.run(debug=False, host="0.0.0.0", port=port)
