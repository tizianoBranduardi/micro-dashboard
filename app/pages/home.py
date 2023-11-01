import os
import dash
from dash import Dash, html, dcc, dash_table
import plotly.express as px
import pandas as pd
from utils.db_connector import engine, query_homepage

dash.register_page(__name__, path='/')

colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}


def serve_layout():
    data = pd.read_sql(query_homepage, engine)
    return html.Div(
        children=[
            html.Br(),
            dash_table.DataTable(data.to_dict('records'),
                                 [{"name": i, "id": i} for i in data.columns],
                                 sort_action="native",
                                 sort_mode='multi',
                                 filter_action="native",
                                 filter_options={"placeholder_text": "Filter column..."},
                                 page_size=20, ),
        ]
    )


layout = serve_layout
