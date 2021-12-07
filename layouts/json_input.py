from dash import html, Output, Input, dcc
from dash.exceptions import PreventUpdate

from components.graph_builder import gb
from app import app

def json_input():

    return (
        html.Div([
            html.Div('Add JSON data', className='fs-3'),
            dcc.Textarea(
                placeholder='paste json data here',
                # value=open('test_json.json').read(),
                className='input-area w-100 my-3',
                rows=20,
                id='json-textarea'
            ),
            html.Button('Load JSON', className='w-100 btn btn-light mb-3', id='json-submit'),
            html.Div(
                'Using JSON data, you can visualize stats that go beyond the default leaderboard.  You can find json '
                'data for your private leaderboard by appending ".json" to the end of your leaderboard url. i.e. if '
                'your leaderboard url is "https://adventofcode.com/2021/leaderboard/private/view/138XXX" you can '
                'access the json by navigating to '
                '"https://adventofcode.com/2021/leaderboard/private/view/138XXX.json" ',
                className=''),
            html.Div([
                html.Div('A few things to note...'),
                html.Ul([
                    html.Li('You cannot see leaderboards you are not a part of'),
                    html.Li('It is impossible to see any more data, other than what is contained within the JSON'),
                    html.Li('This project is not affiliated with Advent of Code'),
                ])
            ], className='m-3'),

        ], className='m-3')
    )

@app.callback(
    [Output("graphs-container", "children"), Output("json-input-container", "children")],
    [Input('json-textarea', 'value'), Input('json-submit', 'n_clicks')],
)
def input_json(value, n_clicks):
    if n_clicks is None:
        raise PreventUpdate

    gb.add_json(value)



    return gb.render(), html.Div()
