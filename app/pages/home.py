import dash
from dash import Dash, html
import dash_bootstrap_components as dbc

dash.register_page(__name__, path='/')

colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}


def serve_layout():
    left_column = html.Div([
        dbc.Button("Report Fatturato - Scope anno",
                   href=dash.page_registry['pages.fatturato_annuale']["relative_path"],
                   outline=True,
                   color="primary",
                   className="me-1"),
        dbc.Button("Upload CSV",
                   href=dash.page_registry['pages.uploadCSV']["relative_path"],
                   outline=True,
                   color="primary",
                   className="me-1")
        ],
        className="d-grid gap-2 col-6 mx-auto"
    )

    right_column = html.Div([
        dbc.Button("Report Fatturato - Scope mese",
                   href=dash.page_registry['pages.fatturato_mensile']["relative_path"],
                   outline=True,
                   color="primary",
                   className="me-1"),
        dbc.Button(dash.page_registry['pages.home']['name'],
                   href=dash.page_registry['pages.home']["relative_path"],
                   outline=True,
                   color="primary",
                   className="me-1",
                   disabled=True)
    ],
        className="d-grid gap-2 col-6 mx-auto"
    )

    return dbc.Row([left_column, right_column], )


layout = serve_layout
