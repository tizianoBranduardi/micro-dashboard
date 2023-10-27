import os
import dash
from dash import Dash, html, dcc, dash_table
import plotly.express as px
import pandas as pd
from utils.db_connector import engine, query_fatturato_paese
from dateutil.parser import parse

dash.register_page(__name__)

colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}


fatturato_per_paese = pd.read_sql(query_fatturato_paese, engine)

layout = html.Div(
    children=[
        html.Br(),
        html.H4(
            children="Fatturato per paese"
        ),
        dash_table.DataTable(fatturato_per_paese.to_dict('records'),
                            [{"name": i, "id": i} for i in fatturato_per_paese.columns],
                            sort_action="native",
                            sort_mode='multi',
                            filter_action="native",
                            filter_options={"placeholder_text": "Filter column..."},
                            page_size=20,),
    ]
)