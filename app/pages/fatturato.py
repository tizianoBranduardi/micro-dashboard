import os
import dash
from dash import Dash, html, dcc, dash_table, callback, Output, Input
import plotly.express as px
import pandas as pd
from utils.db_connector import engine, query_fatturato
from dateutil.parser import parse

dash.register_page(__name__)

colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}


sales = pd.read_sql(query_fatturato, engine)
sales['data'] = pd.to_datetime(sales['data'], format='%Y/%m/%d', utc=False)

clienti = sales["ragione_sociale"].sort_values().unique()
date = sales["data"].sort_values().unique()


layout = html.Div(
    children=[
        html.Br(),
        html.H4(
            children="Fatturato"
        ),
        dash_table.DataTable(sales.to_dict('records'),
                             [{"name": i, "id": i} for i in sales.columns],
                             sort_action="native",
                             sort_mode='multi',
                             filter_action="native",
                             filter_options={"placeholder_text": "Filter column..."},
                             page_size=5, ),
        html.Div(
            children=[
                # html.Div(
                #     children=[
                #         html.Div(children="Clienti", className="menu-title"),
                #         dcc.Dropdown(
                #             id="region-filter",
                #             options=[
                #                 {"label": cliente, "value": cliente}
                #                 for cliente in clienti
                #             ],
                #             clearable=False,
                #             className="dropdown",
                #         ),
                #     ]
                # ),
                html.Div(
                    children=[
                        html.Div(
                            children="Date"  # , className="menu-title"
                        ),
                        dcc.DatePickerRange(
                            id="date-range",
                            min_date_allowed=sales["data"].min(),
                            max_date_allowed=sales["data"].max(),
                            start_date=sales["data"].min(),
                            end_date=sales["data"].max(),
                        ),
                    ]
                ),
            ],
            className="menu",
        ),
        html.Div(
            children=[
                html.Div(
                    children=dcc.Graph(
                        id="sales_graph",
                        config={"displayModeBar": False},
                    ),
                    className="card",
                ),
                html.Div(
                    children=dcc.Graph(
                        id="quarter_graph",
                        config={"displayModeBar": False},
                    ),
                    className="card",
                )
            ],
            className="wrapper",
        ),
    ]
)


@callback(
    Output("sales_graph", "figure"),
    [Input("date-range", "start_date"),
     Input("date-range", "end_date")]
)
def update_sale_graph(start_date, end_date):
    if not start_date or not end_date:
        raise dash.exceptions.PreventUpdate
    else:
        mask = (sales['data'] > start_date) & (sales['data'] <= end_date)
        sales_filtered = sales.loc[mask]
        sales_per_year_filtered = (sales_filtered.groupby(sales_filtered.data.dt.year)['total'].sum()
                                   .reset_index()  # Rimozione multi index
                                   .rename(columns={'data': 'Anno', 'total': 'Totale'}))
        return px.bar(sales_per_year_filtered,
                      title="Fatturato",
                      x='Anno',
                      y='Totale')


@callback(
    Output("quarter_graph", "figure"),
    [Input("date-range", "start_date"),
     Input("date-range", "end_date")]
)
def update_quarter_graph(start_date, end_date):
    if not start_date or not end_date:
        raise dash.exceptions.PreventUpdate
    else:
        mask = (sales['data'] > start_date) & (sales['data'] <= end_date)
        sales_filtered = sales.loc[mask]
        sales_per_quarter_filtered = (sales_filtered.groupby(sales_filtered.data.dt.to_period('Q'))['total'].sum()
                                      .reset_index()  # Rimozione multi index
                                      .rename(columns={'data': 'Anno', 'total': 'Totale'}))
        sales_per_quarter_filtered['Quarter'] = sales_per_quarter_filtered['Anno'].astype(str).str[-1]
        sales_per_quarter_filtered['Anno'] = sales_per_quarter_filtered['Anno'].astype(str).str[:4]

        return px.bar(sales_per_quarter_filtered,
                      title="Fatturato per quarter",
                      color='Quarter',
                      barmode="group",
                      x='Anno',
                      y='Totale')
