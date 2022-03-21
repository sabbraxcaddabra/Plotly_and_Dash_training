# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import dash
from dash import dcc
from dash import html
import plotly.express as px
import pandas as pd


def load_layout():
    with open('simple_header.txt', 'r', encoding='utf8') as f:
        header_text = f.readline()
        header_text = header_text.strip()

    colors = {
        'background': 'white',
        'text': 'black'
    }
    external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

    df = pd.DataFrame({
        "Fruit": ["Apples", "Oranges", "Bananas", "Apples", "Oranges", "Bananas"],
        "Amount": [4, 1, 2, 2, 4, 5],
        "City": ["SF", "SF", "SF", "Montreal", "Montreal", "Montreal"]
    })

    fig = px.bar(df, x="Fruit", y="Amount", color="City", barmode="group")

    fig.update_layout(
        plot_bgcolor=colors['background'],
        paper_bgcolor=colors['background'],
        font_color=colors['text']
    )

    layout = html.Div(style={'backgroundColor': colors['background']}, children=[
        html.H1(
            children=header_text,
            style={
                'textAlign': 'center',
                'color': colors['text']
            }
        ),

        html.Div(children='Dash: A web application framework for your data.', style={
            'textAlign': 'center',
            'color': colors['text']
        }),

        dcc.Graph(
            id='example-graph-2',
            figure=fig
        )
    ])
    return layout



app = dash.Dash(__name__)

app.layout = load_layout

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options


if __name__ == '__main__':
    app.run_server(debug=True)