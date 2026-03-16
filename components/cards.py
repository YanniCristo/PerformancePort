from dash import html
import dash_bootstrap_components as dbc


def cards_home():

    data = [
        ("/assets/contents/home/dollar.png", "Explore the value of Indipendent Investing"),
        ("/assets/contents/home/center.png", "Understand how Time Horizon and investor risk profile shape allocation models"),
        ("/assets/contents/home/line.png", "See how Market Cycles drives investments allocation"),
        ("/assets/contents/home/bars.png", "Stay informed with a coincise Economic Overview - see at a glance what drives our macro allocation"),
        ("/assets/contents/home/user.png", "Discover the current Market Phase and how it drives Macro Asset Allocation across risk profiles"),
        ("/assets/contents/home/folder.png", "Access Leading Equity Markets Allocation - built from a selection of top index constituents, dynamically adjusted each month and benchmarked against their reference indices")]

    cards = [
        dbc.Col(
            dbc.Card(
                dbc.CardBody([
                    html.Img(src=title, style={"height": "40px"}, className="card-icon"),
                    html.H1(value)
                ]),
                className="metric-card"
            ),
            md=4,
            className="mb-4"
        )
        for title, value in data
    ]

    return dbc.Container(
        dbc.Row(cards),
        className="mt-5"
    )





