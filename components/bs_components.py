from dash import html


def container(children):
    return (
        html.Div(children, className='container')
    )


def row(children):
    return (
        html.Div(children, className='row')
    )
