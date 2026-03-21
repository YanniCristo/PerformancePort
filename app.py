from callbacks.pages_callbacks import register_callbacks
from callbacks.login_callbacks import login_callbacks
from callbacks.theme_callbacks import theme_callbacks
from callbacks.chart_callbacks import chart_callbacks
from callbacks.navbar_callbacks import navbar_callbacks
from callbacks.macro_callbacks import macro_callbacks
from layouts.main_layout import create_layout

import dash_bootstrap_components as dbc
from dash import Dash
import os

app = Dash(__name__,
           title="PerformancePort.com",
           external_stylesheets=[dbc.themes.CYBORG])

server = app.server

login_callbacks(app)
register_callbacks(app)
theme_callbacks(app)
navbar_callbacks(app)
chart_callbacks(app)
macro_callbacks(app)

app.layout = create_layout()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 9000))
    app.run(debug=False, host="0.0.0.0", port=port)
