import os
import dash
from dash import Dash, html, dcc, dash_table
import plotly.express as px
import pandas as pd
from utils.db_connector import conn, query_homepage

debug = False if os.environ["DASH_DEBUG_MODE"] == "False" else True

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = Dash(__name__, use_pages=True, external_stylesheets = external_stylesheets)

server = app.server

app.layout = html.Div(
    children=[
        html.H1(
            children=f"BigDB - {'Versione di sviluppo' if debug else 'Versione di produzione'}"
        ),
        html.Div([
            html.Div(
                dcc.Link(f"{page['name']} - {page['path']}", href=page["relative_path"])
            ) for page in dash.page_registry.values()
        ]),
        dash.page_container
    ]
)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port="8050", debug=debug, threaded=True)
