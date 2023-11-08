import os
import dash
from dash import Dash, html, dcc, dash_table
import plotly.express as px
import pandas as pd
from utils.db_connector import engine, query_cliente
from dateutil.parser import parse

dash.register_page(__name__)

colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}


def serve_layout():
    clienti = pd.read_sql(query_cliente, engine)

    layout = html.Div(
        children=[
            html.Br(),
            html.H4(
                children="Clienti"
            ),
            dash_table.DataTable(clienti.to_dict('records'),
                                 [{"name": i, "id": i} for i in clienti.columns],
                                 sort_action="native",
                                 sort_mode='multi',
                                 filter_action="native",
                                 filter_options={"placeholder_text": "Filter column..."},
                                 page_size=20, ),
        ]
    )
    return layout


layout = serve_layout
