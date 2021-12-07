from dash import html

from components.bs_components import container, row
from components.navbar import nav_bar
from layouts.graphs import graphs_layout
from layouts.json_input import json_input


def home_layout():
    return (
        html.Div([
            nav_bar(),
            container([
                row([
                    html.Div(json_input(), id='json-input-container'),
                    html.Div(id='graphs-container')
                ])
            ])
        ])

    )