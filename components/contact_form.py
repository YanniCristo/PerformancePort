from dash import html, dcc
import dash_bootstrap_components as dbc

def contact_form():
    return dbc.Container(
        [
            html.H5("INFORMATION REQUEST", className="mb-4 text-white"),
            
            dbc.Row([
                dbc.Col(dbc.Input(placeholder="Name"), md=6, className="mb-3"),
                dbc.Col(dbc.Input(placeholder="Surname"), md=6, className="mb-3"),
            ]),
            
            dbc.Row([
                dbc.Col(dbc.Input(placeholder="City"), md=6, className="mb-3"),
                dbc.Col(dbc.Input(placeholder="E-mail"), md=6, className="mb-3")
            ]),

            dbc.Row([
                dbc.Col(dbc.Input(placeholder="Number"), md=6, className="mb-3")
            ]),

            dbc.Textarea(
                placeholder="Write your request here",
                className="mb-3"
            ),

            dbc.Checklist(
                options=[
                    {"label": "I have read and agree to the Privacy Policy", "value": 1},
                    {"label": "I agree to receive the periodic newsletter and the processing of my personal data for this purpose.", "value": 2},
                ],
                value=[],
                inline=False,
                className="mb-3 text-white"
            ),

            dbc.Button(
                [html.Span("Send"), html.I(className="ms-2 bi bi-arrow-right")],
                color="light",
                className="w-100"
            )

        ],
        className="p-4",
        style={
            "background-color": "#1D4B8C",  # colore blu come nell'immagine
            "border-radius": "12px",
            "color": "white"
        }
    )

