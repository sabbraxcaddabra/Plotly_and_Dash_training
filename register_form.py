from dash import dcc
from dash import html
import dash

from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate

import json

import dash_bootstrap_components as dbc

def get_regions_and_schools():
    with open('all_region_schools.json', encoding='utf8') as f:
        region_and_schools = json.load(f)

    return region_and_schools


def get_regions():
    with open('regions.txt') as f:
        lines = [line.strip() for line in f.readlines()]

    return lines

region_and_schools = get_regions_and_schools()
regions = list(region_and_schools.keys())


external_stylesheets = [
    dbc.themes.BOOTSTRAP,
    dbc.themes.GRID,
    'https://codepen.io/chriddyp/pen/bWLwgP.css'
]
app = dash.Dash(
    __name__,
    external_stylesheets=external_stylesheets,
    meta_tags=[{'name': 'viewport', 'content': 'width=device-width, initial-scale=1'}]
)


app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.Div("Регистрация на день открытых дверей",
                         style={'textAlign': 'center', 'fontSize': '18px'}))
    ]),
    dbc.Row([
        html.H4('1. Фамилия, имя, отчество'),
        dbc.Col(dbc.Input(placeholder='Фамилия', id='surname', size='lg')),
        dbc.Col(dbc.Input(placeholder='Имя', id='name',size='lg')),
        dbc.Col(dbc.Input(placeholder='Отчество', id='f_name', size='lg'))
    ]),
    dbc.Row([
        html.H4('2. Регион'),
        dcc.Dropdown(options=regions, value=regions[0], placeholder='Начните набирать...', id='region')
    ]),
    dbc.Row([
        html.H4('3. Образовательное учреждение'),
        dcc.Dropdown(options=[], id='school')
    ])
])

@app.callback(
    Output('school', 'options'),
    [Input('region', 'value')]
)
def update_schools(region):
    return region_and_schools[region]

if __name__ == "__main__":
    # app.run_server(debug=True)
    # app.run_server('172.24.135.27', debug=True)
    app.run_server('192.168.0.188', debug=True)