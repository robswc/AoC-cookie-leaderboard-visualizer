import datetime
import json

import pytz
from dash import html, dash_table, dcc, Output, Input
import pandas as pd
from dash.exceptions import PreventUpdate

from app import app

import plotly.graph_objects as go


class GraphBuilder():
    def __init__(self):
        self.json_data = None
        self.total_days = 0

    def add_json(self, data):
        try:
            self.json_data = json.loads(data)
        except Exception as e:
            print(e)
            return 'Error'

    def build_leaderboard_data(self):

        members = self.json_data.get('members')

        rows = []
        for member, stats in members.items():
            rows.append(
                {
                    'id': stats.get('id'),
                    'stars': stats.get('stars', 0),
                    'local_score': stats.get('local_score', 0),
                    'Name': stats.get('name', 'None'),
                }
            )

        df = pd.DataFrame(rows)
        df = df.drop(['id'], axis=1)
        df.columns = ['Stars', 'Score', 'Name']
        df = df[['Name', 'Stars', 'Score']]
        df = df.sort_values(by=['Score'], ascending=False)
        print(df.head())

        return df

    def render_leaderboard(self, df):
        return (
            html.Div([
                dash_table.DataTable(
                    id='table',
                    columns=[{"name": i, "id": i} for i in df.columns],
                    data=df.to_dict('records'),
                    sort_action="native",
                    sort_mode="multi",
                    style_as_list_view=True,
                    style_cell={'padding': '5px', 'backgroundColor': '#10101a', 'border': '1px solid #333340'},
                    style_header={
                        'backgroundColor': '#10101a',
                        'color': 'white',
                        'fontWeight': 'bold'
                    },
                    style_cell_conditional=[
                        {
                            'if': {'column_id': c},
                            'textAlign': 'left'
                        } for c in ['Name']
                    ],
                )
            ], style={'border': '1px solid #333340'})
        )

    def render_daily_breakdown(self, day, start, end, sort):

        members = self.json_data.get('members')

        silver = None
        gold = None

        rows = []
        for member, stats in members.items():

            try:
                silver = stats.get('completion_day_level').get(str(day)).get('1').get('get_star_ts', 0)
            except:
                silver = 0

            try:
                gold = stats.get('completion_day_level').get(str(day)).get('2').get('get_star_ts', 0)
            except:
                gold = 0

            if silver != 0 and gold != 0:
                rows.append(
                    {
                        'silver': silver,
                        'gold': gold,
                        'diff': gold - silver,
                        'name': stats.get('name', 'None'),
                    }
                )
                self.total_days += 1

        df = pd.DataFrame(rows)
        df = df.sort_values(by=[sort], ascending=False)

        fig = go.Figure()
        fig.add_trace(go.Bar(
            y=df['name'].values.tolist(),
            x=[v - start for v in df['silver'].values.tolist()],
            name='Silver',
            orientation='h',
            marker=dict(
                color='#9999cc',
            )
        ))
        fig.add_trace(go.Bar(
            y=df['name'].values.tolist(),
            x=df['diff'].values.tolist(),
            name='Gold',
            orientation='h',
            marker=dict(
                color='#ffff66',
            )
        ))

        fig.update_layout(barmode='stack', plot_bgcolor='#10101a', paper_bgcolor='#10101a', font_color="#cccccc",
                          margin={'pad': 20}, xaxis_tickformat='%d %B (%a)<br>%Y', title='Time to Complete (in Seconds)')
        fig.update_xaxes(range=[0, end - start], linecolor='#10101a')
        fig.update_yaxes(linecolor='#10101a')

        return (
            [
                dcc.Graph(figure=fig, style={'width': '100%', 'height': '200vh', 'border': '1px solid #333340'})
            ]
        )

    def render(self):
        if self.json_data is None:
            return (
                html.Div('No data')
            )

        tabs = dcc.Tabs([
            dcc.Tab(label='Leaderboard', children=[
                html.Div([
                    self.render_leaderboard(self.build_leaderboard_data())
                ])
            ], className='custom-tab', selected_className='custom-tab--selected'),
            dcc.Tab(label='Daily Breakdown', children=[
                html.Div([
                    html.Div([
                        html.Div('Date Range', className='fs-5'),
                        dcc.DatePickerRange(id='input-breakdown-range', className='w-100'),
                    ], className='col'),
                    html.Div([
                        html.Div('Day'),
                        dcc.Dropdown(id='input-breakdown-day', placeholder='Select Day',
                                     options=[{'label': i, 'value': i} for i in range(0, 25)]),
                        html.Div('Sort by Gold, Silver or Difference'),
                        dcc.Dropdown(id='input-breakdown-sort', placeholder='Select Sorting',
                                     options=[{'label': i, 'value': i} for i in ['gold', 'silver', 'diff']],
                                     value='gold'
                                     ),
                    ], className='col'),
                ], className='row my-3'),
                html.Div(id='breakdown-container')
            ], className='custom-tab', selected_className='custom-tab--selected'),
            dcc.Tab(label='All Time', disabled=True, children=[
                dcc.Graph(
                    figure={
                        'data': [
                            {'x': [1, 2, 3], 'y': [2, 4, 3],
                             'type': 'bar', 'name': 'SF'},
                            {'x': [1, 2, 3], 'y': [5, 4, 3],
                             'type': 'bar', 'name': u'Montréal'},
                        ]
                    }
                )
            ]),
        ])

        return (tabs)


gb = GraphBuilder()


@app.callback(
    [Output("breakdown-container", "children")],
    [Input('input-breakdown-range', 'start_date'), Input('input-breakdown-range', 'end_date'),
     Input('input-breakdown-day', 'value'), Input('input-breakdown-sort', 'value')],
)
def input_json(start, end, day, sort):
    if start is None or end is None:
        raise PreventUpdate

    timezone = pytz.timezone("EST")
    start_ts = datetime.datetime.strptime(start, '%Y-%m-%d')
    start_ts = timezone.localize(start_ts).timestamp()
    end_ts = datetime.datetime.strptime(end, '%Y-%m-%d')
    end_ts = timezone.localize(end_ts).timestamp()

    return gb.render_daily_breakdown(day, start_ts, end_ts, sort)
