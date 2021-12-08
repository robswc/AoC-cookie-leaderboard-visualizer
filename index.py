from dash.dependencies import Input, Output
from dash import dcc
from app import app
from dash import html

from layouts.home import home_layout

# create server
server = app.server

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])


@app.callback(Output('page-content', 'children'),
              Input('url', 'pathname'))
def display_page(pathname):
    print(pathname)
    if pathname == '/' or pathname == '' or pathname == '/home':
        return home_layout()
    else:
        return '404'


if __name__ == '__main__':
    app.run_server(debug=True)
