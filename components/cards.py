from dash import html
import dash_bootstrap_components as dbc


def cards_home(txt):
    data = txt['cards']

    cards = [
        dbc.Col(
            dbc.Card(
                dbc.CardBody([
                    html.Img(src=item[0], style={"height": "40px"}, className="card-icon"),
                    html.H1(item[1])
                ]),
                className="metric-card"
            ),
            md=4,
            className="mb-4"
        )
        for key, item in data.items()
    ]

    return dbc.Container(
        dbc.Row(cards),
        className="mt-5"
    )





