import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import plotly

from dash import dcc
from dash import html
import dash
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate

import dash_bootstrap_components as dbc

enrolled = pd.read_csv('enrolled_21.csv', index_col=0)

enrolled_ege = enrolled[enrolled['Кол-во ЕГЭ'] == 3].drop(columns=['Экз магистратуры', 'Тип Экз магистратуры'])

bac_and_spec = enrolled.loc[(enrolled['Уровень'] == 0) | (enrolled['Уровень'] == 1)]
magisters = enrolled.loc[enrolled['Уровень'] == 2]

sum_count_mags = magisters.groupby(['Укрупненная группа'], as_index=False).agg({'id':'count'})
sum_count_bac_and_spec = bac_and_spec.groupby(['Укрупненная группа'], as_index=False).agg({'id':'count'})

u_group_peoples = {
    'Магистратура': sum_count_mags,
    'Бакалавриат и Специалитет': sum_count_bac_and_spec
}

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.H1("Статистика приема абитуриентов БГТУ им. Д.Ф. Устинова \"Военмех\"", style={'textAlign': 'center'})
        ])
    ]),

    dbc.Row([
        dbc.Col([
            html.H2("Число зачисленных по укрупненным группам"),
            dcc.Dropdown(
                id="form_dropdown",
                options=[
                    {"label": "Бакалавриат и Специалитет", "value": "Бакалавриат и Специалитет"},
                    {"label": "Магистратура", "value": "Магистратура"}
                ],
                value=['Бакалавриат и Специалитет'],
                multi=True
            ),
            dcc.Graph(id="u_group_pie_plot"),
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
                value=[30, 100]
            ),
            dcc.Graph('ege_graph'),
        ])
    ]),
    dbc.Row([
        dbc.Col([
            html.H2('Соотношение абитуриентов, сдающих ЕГЭ или экзамен вуза по Физике, Информатике и Обществознанию'),
            dcc.Checklist(
                id="exam_checklist",
                options=[{'label':typ, 'value':typ} for typ in ['Русский', 'Математика', 'Информатика', 'Физика', 'Общество', 'Иностранный', 'Биология']],
                value=['Физика', 'Информатика', 'Общество'],
                labelStyle={'display': 'inline-block'}
            ),
            dcc.Graph(id='exam_dist')
        ])
    ])
])

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
    fig.update_layout(autosize=False, width=1200, height=500)
    return fig

@app.callback(
    Output("ege_graph", "figure"),
    [Input("ege_slider", "value")]
)
def update_ege_hist(value=[30, 100]):
    ege_tmp = enrolled_ege.loc[(enrolled_ege['Ср Балл ЕГЭ'] >= value[0]) & (enrolled_ege['Ср Балл ЕГЭ'] <= value[1])]
    fig = px.histogram(ege_tmp, x='Ср Балл ЕГЭ')

    #fig.update_traces(opacity=0.85)
    fig.update_layout(bargap=0.1, barmode='overlay',
                      xaxis_title="Средний балл ЕГЭ", yaxis_title="Кол-во",
                      autosize=False, width=1200, height=500)

    fig.update_xaxes(showgrid=True)
    fig.update_layout(bargap=0.1)
    return fig

@app.callback(
    Output("u_group_pie_plot", "figure"),
    [Input("form_dropdown", "value")]
)
def update_plot(value):
    n_rows = len(value)
    if not value:
        return make_subplots(cols=1, rows=1)
    else:
        fig = make_subplots(cols=1, rows=n_rows,
                            specs=[[{'type':'domain'}] for _ in range(n_rows)],
                            subplot_titles=value,
                            vertical_spacing=0.05
                            )
        for num, val in enumerate(value, start=1):
            sum_count = u_group_peoples[val]
            fig.add_trace(go.Pie(labels=sum_count['Укрупненная группа'],
                                 values=sum_count['id'], name=val), num, 1)

        fig.update_traces(hole=.1, hoverinfo="label+percent+name")
        fig.update_layout(autosize=False, width=1400, height=500*n_rows,
                          legend=dict(
                              y=0.5,
                              font=dict(
                                  size=16,
                                  color="black"),
                          ))
        return fig

if __name__ == "__main__":
    app.run_server(debug=True)