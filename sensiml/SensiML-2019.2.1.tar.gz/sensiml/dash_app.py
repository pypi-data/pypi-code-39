# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import pandas as pd
import plotly.graph_objs as go
import os
import mydcc
import json

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
project_dir = r'C:\Users\cknorowski\Documents\SensiML\Projects\SensorExpoDemo\data'

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
max_range = 10000
tmp_df = None

app.layout = html.Div(children=[
    html.H1(children='Hello Dash'),

    html.Div(children='''
        Analytics Studio Dashboard: A Graphical Interface to Analytics Studio
    '''),

    dcc.Dropdown(id='file_selector',
                 options=[{'label': x, 'value': x} for x in os.listdir(
                    project_dir)],
                 ),

    mydcc.Relayout(id="graph_layout", aim='graph'),
    dcc.Graph(id='graph'),

    # Hidden div inside the app that stores the intermediate value
    html.Div(id='intermediate-value', style={'display': 'none'}),

    html.P([
        dcc.RangeSlider(id='slider',
                        min=0,
                        max=max_range,
                        value=[0, max_range])
    ], style={'width': '80%',
              'fontSize': '20px',
              'padding-left': '100px',
              'display': 'inline-block'})
])


@app.callback(
    Output(component_id='graph', component_property='figure'),
    [Input(component_id='file_selector', component_property='value')]
)
def update_figure(file_selector):
    if file_selector is None:
        return {}

    tmp_df = pd.read_csv(os.path.join(project_dir, file_selector))

    data = go.Scattergl(
        y=tmp_df['LTC1859_MayhewA'],
        mode='lines',
        opacity=0.7,
    )

    return {
        'data': [data],
        'layout': go.Layout(
            xaxis={'title': 'Time'},
            yaxis={'title': 'Vibration'},
            margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
            legend={'x': 0, 'y': 1},
            hovermode='closest',
        )
    }


@app.callback(
    Output(component_id='intermediate-value', component_property='children'),
    [Input(component_id='file_selector', component_property='value')]
)
def update_figure_data_graph_1(file_selector):
    return update_figure_data(file_selector)


@app.callback(
    Output(component_id='graph_layout', component_property='layout'),
    [Input(component_id='slider', component_property='value'),
     Input('intermediate-value', 'children')]
)
def update_figure_axis_graph_1(value, graph_data):
    return update_figure_axis(value, graph_data)


def update_figure_data(file_selector):

    if file_selector is None:
        return {}

    tmp_df = pd.read_csv(os.path.join(project_dir, file_selector))

    return {'data_shape': tmp_df.shape}


def update_figure_axis(value, graph_data):

    print(graph_data, type(graph_data))
    if graph_data.get('data_shape', None) is None:
        return {}

    shape = graph_data['data_shape']
    print(value)

    return {"xaxis": {'range': [int(value[0]/max_range*shape[0]), int(value[1]/max_range*shape[0])]},
            }


if __name__ == '__main__':
    app.run_server(debug=True)
