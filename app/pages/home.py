import dash
from dash import Dash, html
import dash_bootstrap_components as dbc

dash.register_page(__name__, path='/')

colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}


def serve_layout():
    left_column = dbc.Col(
        html.Div([
            html.Div([
                dbc.Button("Report Fatturato",
                           # dash.page_registry['pages.home']['name'],
                           href=dash.page_registry['pages.fatturato']["relative_path"],
                           outline=True,
                           color="primary",
                           className="me-1")
            ],
                style={'width': '100 %', 'display': 'flex', 'align - items': 'center', 'justify - content': 'center'}
            ),
            html.Br(),
            html.Div([
                dbc.Button(dash.page_registry['pages.home']['name'],
                           href=dash.page_registry['pages.home']["relative_path"],
                           outline=True,
                           color="primary",
                           className="me-1",
                           disabled=True)
            ],
                style={'width': '100 %', 'display': 'flex', 'align - items': 'center', 'justify - content': 'center'}
            ),
        ]),
        align="center"
    )

    right_column = dbc.Col(
        html.Div([
            html.Div([
                dbc.Button("Upload CSV",
                           # dash.page_registry['pages.home']['name'],
                           href=dash.page_registry['pages.uploadCSV']["relative_path"],
                           outline=True,
                           color="primary",
                           className="me-1")
            ]),
            html.Br(),
            html.Div([
                dbc.Button(dash.page_registry['pages.home']['name'],
                           href=dash.page_registry['pages.home']["relative_path"],
                           outline=True,
                           color="primary",
                           className="me-1",
                           disabled=True)
            ]),
        ]),
        md=6,
    )

    return dbc.Row([left_column, right_column], className="align-items-md-stretch")


layout = serve_layout
