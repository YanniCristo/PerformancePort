from dash import html
import dash_bootstrap_components as dbc

def cards():

    return dbc.Container([
        dbc.Row([
            dbc.Col(dbc.Card(
                dbc.CardBody([
                    html.H4("Perf. YtD"),
                    html.H2("12,40%")
                ])
            )),
            dbc.Col(dbc.Card(
                dbc.CardBody([
                    html.H4("Perf. since inception"),
                    html.H2("22,43%")
                ])
            )),
            dbc.Col(dbc.Card(
                dbc.CardBody([
                    html.H4("Standard Deviation"),
                    html.H2("14.3%")
                ])
            ))
        ])
    ], className="mt-4")
