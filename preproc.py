import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import plotly
from faker import Faker
import datetime

from dash import dcc
from dash import html
import dash
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate

import dash_bootstrap_components as dbc
from dash_bootstrap_templates import ThemeSwitchAIO

# select the Bootstrap stylesheet2 and figure template2 for the theme toggle here:
template_theme1 = "flatly"
template_theme2 = "darkly"
url_theme1 = dbc.themes.FLATLY
url_theme2 = dbc.themes.DARKLY


def gen_rand_date(size):
    fkr = Faker()
    fkr_data = []
    start = datetime.date(year=2021, month=7, day=15)
    stop = datetime.date(year=2021, month=8, day=15)
    for _ in range(size):
        fkr_data.append(fkr.date_between_dates(start, stop))
    return pd.to_datetime(fkr_data)


df = pd.read_excel("Зачисленные 21.xlsx", sheet_name=0)
df.dropna(subset=['Код'], inplace=True)
df['Дата'] = gen_rand_date(df.shape[0])
df['Уровень'], lev_unique = pd.factorize(df['Уровень'])
df['БВИ/Право'], bvi_unique = pd.factorize(df['БВИ/Право'])
df['Основание/Условие'], reason_unique = pd.factorize(df['Основание/Условие'])
df['Форма'], form_unique = pd.factorize(df['Форма'])
df.drop(columns=['Приказ'], inplace=True)

df['Укрупненная_группа'] = [item.split('.')[0] for item in df['Код']]

bac_and_spec = df.loc[(df['Уровень'] == 0) | (df['Уровень'] == 1)]
magisters = df.loc[df['Уровень'] == 2]

u_group_peoples = {
    'Магистратура':magisters,
    'Бакалавриат+Специалитет': bac_and_spec
}

ege_only = bac_and_spec.loc[bac_and_spec['Кол-во ЕГЭ'] == 3]


fig = make_subplots(rows=2, cols=2, shared_yaxes=True)

fig.add_trace(go.Scatter(x=[1, 2, 3], y=[2, 3, 4]),
              row=1, col=1)

# sum_counts_ege = ege_only.groupby(['Укрупненная_группа']).count()['id']
# sum_counts_mag = magisters.groupby(['Укрупненная_группа']).count()['id']
#
# fig = px.pie(values=sum_counts_ege, names=sum_counts_ege.index, hole=0.6)
# fig.add_annotation(x=0.5, y=0.5, text='Год 2021', showarrow=False)
# fig2 = px.pie(values=sum_counts_mag, names=sum_counts_mag.index, hole=0.7)
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)


app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.H1("Статистика приема абитуриентов БГТУ им. Д.Ф. Устинова \"Военмех\"", style={'textAlign': 'center'}),
        ])
    ]),

    dbc.Row([
        dbc.Col([
            html.H2("Число заявлений по укрупненным группам"),
            dcc.Dropdown(
                id="form_dropdown",
                options=[
                    {"label": "Бакалавриат+Специалитет", "value": "Бакалавриат+Специалитет"},
                    {"label": "Магистратура", "value": "Магистратура"}
                ],
                value=['Бакалавриат+Специалитет'],
                multi=True
            ),
            dcc.Graph(id="u_group_pie_plot"),
        ])
    ]),
    dbc.Row([
        dbc.Col([
            html.H2("Распределение заявлений по дням"),
            dcc.DatePickerRange(
                id='pick_a_date',
                start_date=datetime.date(year=2021, month=7, day=15),
                end_date=datetime.date(year=2021, month=8, day=15),
                max_date_allowed=datetime.date(year=2021, month=8, day=15),
                min_date_allowed=datetime.date(year=2021, month=7, day=15)
            ),
            dcc.Graph(id='time_series_graph'),
        ])
    ]),
    dbc.Row([
        dbc.Col([
            html.H2("Распределение абитуриентов по среднему баллу ЕГЭ"),
            dcc.RangeSlider(
                id='ege_slider',
                min=30,
                max=100,
                step=None,
                marks={num:f'{num}' for num in range(30, 105, 5)},
                value=[50, 90]
            ),
            dcc.Graph('ege_graph'),
        ])
    ]),
    dbc.Row([
        dbc.Col([
            html.H2('Соотношение абитуриентов, сдающих ЕГЭ или экзамен вуза по разным предметам'),
            dbc.Checklist(
                id="exam_checklist",
                options=[{'label':typ, 'value':typ} for typ in ['Русский', 'Математика', 'Информатика', 'Физика', 'Общество', 'Иностранный', 'Биология']],
                value=['Русский', 'Математика'],
                inline=True
            ),
            dcc.Graph(id='exam_dist')
        ])
    ])
])



# app.layout = html.Div([
#     html.H1("Статистика приема абитуриентов БГТУ им. Д.Ф. Устинова \"Военмех\"", style={'textAlign': 'center'}),
#     html.H2("Число заявлений по укрупненным группам"),
#     dcc.Dropdown(
#         id="form_dropdown",
#         options=[
#             {"label": "Бакалавриат+Специалитет", "value": "Бакалавриат+Специалитет"},
#             {"label": "Магистратура", "value": "Магистратура"}
#         ],
#         value=['Бакалавриат+Специалитет'],
#         multi=True
#     ),
#     dcc.Graph(id="u_group_pie_plot"),
#     html.H2("Распределение заявлений по дням"),
#     dcc.DatePickerRange(
#         id='pick_a_date',
#         start_date=datetime.date(year=2021, month=7, day=15),
#         end_date=datetime.date(year=2021, month=8, day=15),
#         max_date_allowed=datetime.date(year=2021, month=8, day=15),
#         min_date_allowed=datetime.date(year=2021, month=7, day=15)
#     ),
#     dcc.Graph(id='time_series_graph'),
#     html.H2("Распределение абитуриентов по среднему баллу ЕГЭ"),
#     dcc.RangeSlider(
#         id='ege_slider',
#         min=30,
#         max=100,
#         step=None,
#         marks={num:f'{num}' for num in range(30, 105, 5)},
#         value=[50, 90]
#     ),
#     dcc.Graph('ege_graph'),
#     html.H2('Соотношение абитуриентов, сдающих ЕГЭ или экзамен вуза по разным предметам'),
#     dcc.Checklist(
#         id="exam_checklist",
#         options=[{'label':typ, 'value':typ} for typ in ['Русский', 'Математика', 'Информатика', 'Физика', 'Общество', 'Иностранный', 'Биология']],
#         value=['Русский', 'Математика']
#     ),
#     dcc.Graph(id='exam_dist')
# ])

@app.callback(
    Output("exam_dist", "figure"),
    [Input("exam_checklist", 'value')]
)
def update_exam_dist(value):
    if not value:
        return make_subplots(cols=1, rows=1)

    grouped_dataframe = pd.DataFrame()
    for num, val in enumerate(value):
        tmp = bac_and_spec.groupby([f'Тип {val}']).count()

        ege = tmp.iloc[0, 0]
        if tmp.shape[0] == 1:
            vus = 0
        else:
            vus = tmp.iloc[1, 0]

        tmp_df = pd.DataFrame({
            'Предмет': [val, val],
            'Кол-во':[ege, vus],
            'Тип':['ЕГЭ', 'Экзамен ВУЗа']
        })
        grouped_dataframe = pd.concat([grouped_dataframe, tmp_df], ignore_index=True)
    fig = px.bar(grouped_dataframe, x="Предмет", y="Кол-во", color="Тип", barmode="group")
    return fig

@app.callback(
    Output("ege_graph", "figure"),
    [Input("ege_slider", "value")]
)
def update_ege_hist(value):
    ege_tmp = ege_only.loc[(df['Ср Балл ЕГЭ'] >= value[0]) & (df['Ср Балл ЕГЭ'] <= value[1])]
    fig = px.histogram(ege_tmp, x='Ср Балл ЕГЭ')
    fig.update_xaxes(showgrid=True)
    fig.update_layout(bargap=0.1)
    return fig

@app.callback(
    Output("time_series_graph", "figure"),
    [Input("pick_a_date", "start_date"), Input("pick_a_date", "end_date")]
)
def update_time_hist(start, end):
    time_range_df = df.loc[(df['Дата'] >= start) & (df['Дата'] <= end)].groupby(['Дата'])
    sum_counts = time_range_df.count()['id']
    fig = px.area(x=sum_counts.index, y=sum_counts)
    fig.update_xaxes(title_text='Дата')
    fig.update_yaxes(title_text='Число заявлений')
    # fig.update_traces(xbins_size="D1")
    # fig.update_xaxes(showgrid=True, ticklabelmode="period", dtick="D1")
    # fig.update_layout(bargap=0.1)
    return fig

@app.callback(
    Output("u_group_pie_plot", "figure"),
    [Input("form_dropdown", "value")]
)
def update_plot(value):
    n_cols = len(value)
    if not value:
        return make_subplots(cols=1, rows=1)
    else:
        fig = make_subplots(cols=n_cols, rows=1, specs=[[{'type':'domain'} for _ in range(n_cols)]])
        for num, val in enumerate(value, start=1):
            sum_count = u_group_peoples[val].groupby(['Укрупненная_группа']).count()['id']
            fig.add_trace(go.Pie(labels=sum_count.index, values=sum_count), 1, num)

        fig.update_traces(hole=.4, hoverinfo="label+percent+name")
        return fig


if __name__ == "__main__":
    app.run_server(debug=True)







