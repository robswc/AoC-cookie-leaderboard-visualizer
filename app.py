import dash

external_stylesheets = [
    'https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css'
]

external_scripts = [
    'https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css'
]

# create app
app = dash.Dash(__name__, external_stylesheets=external_stylesheets, external_scripts=external_scripts,
                suppress_callback_exceptions=True)

# set title
app.title = 'AoC Cookie Leaderboard'

# create server
server = app.server

