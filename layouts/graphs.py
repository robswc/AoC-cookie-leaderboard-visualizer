from dash import html

from components.graph_builder import gb


def graphs_layout():
    return (
        html.Div([
            gb.render()
        ])
    )