from dash import html


def gen_link(text, url, color='green-text'):
    """
    Create a html Link object, given text and url
    :param color: css class for text color, default green
    :param text: Display text
    :param url: url to link to
    :return: html.Div()
    """
    return (
        html.A(f'[{text}]', href=url, className=f'p-2 text-decoration-none {color} link-light')
    )


def nav_bar():
    return (
        html.Div([
            html.Div([
                html.Div([
                    html.Div([
                        html.Div('$ Advent of Code', className='green-text-glow fs-1', style={'fontWeight': '300'}),
                        html.Div('(Cookie) Leaderboard', className='green-text fs-3', style={'fontWeight': '300'}),
                    ], className='d-flex flex-column'),
                    # html.Div([
                    #     html.Div('(not affiliated with Advent of Code)', className='gray-text ps-1')
                    # ], className='d-flex')
                ], className='p-3 col-lg-4'),
                html.Div([
                    gen_link('Advent of Code', 'https://adventofcode.com/'),
                    gen_link('About', '/about'),
                    gen_link('Github', 'https://github.com/robswc/AoC-cookie-leaderboard-visualizer'),
                    gen_link('created by @robswc', 'https://twitter.com/robswc', color='gray-text'),
                ], className='pl-5 col-lg-8')
            ], className='d-flex align-items-center row justify-content-center')
        ], className='container')
    )
