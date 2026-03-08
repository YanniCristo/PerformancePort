from callbacks.login_callbacks import login_callbacks
from callbacks.pages_callbacks import register_callbacks
from layouts.main_layout import create_layout
import dash_bootstrap_components as dbc
import functions as fnc
from dash import Dash

app = Dash(__name__, external_stylesheets=[dbc.themes.CYBORG])
server = app.server

login_callbacks(app)
register_callbacks(app)

app.layout = create_layout()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8050))
    app.run(debug=False, host="0.0.0.0", port=port)
