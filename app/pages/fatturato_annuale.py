import dash
import pandas as pd
import plotly.express as px
from dash import html, dcc, dash_table, callback, Output, Input
from utils.db_connector import engine, query_fatturato

dash.register_page(__name__)

colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}

sales = pd.read_sql(query_fatturato, engine)
sales['data'] = pd.to_datetime(sales['data'], format='%Y/%m/%d', utc=False)

clienti = sales["ragione_sociale"].sort_values().unique()
dates = sales["data"].sort_values().unique()

layout = html.Div(
    children=[
        html.Br(),
        html.H4(
            children="Analisi Fatturato - Scope anno"
        ),
        html.Br(),
        # dcc.RangeSlider(
        #     min=1,
        #     max=12,
        #     step=None,
        #     marks={
        #         1: 'Gennaio',
        #         2: 'Febbraio',
        #         3: 'Marzo',
        #         4: 'Aprile',
        #         5: 'Maggio',
        #         6: 'Giugno',
        #         7: 'Luglio',
        #         8: 'Agosto',
        #         9: 'Settembre',
        #         10: 'Ottobre',
        #         11: 'Novembre',
        #         12: 'Dicembre',
        #     },
        #     value=[1, 12],
        #     allowCross=False
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
        html.Br(),
        # dash_table.DataTable(id="sales_table",
        #                      sort_action="native",
        #                      sort_mode='multi',
        #                      filter_action="native",
        #                      filter_options={"placeholder_text": "Filter column..."},
        #                      page_size=5, ),
        html.Div(
            children=[
                html.Div(
                    children=dcc.Graph(
                        id="sales_graph",
                        config={"displayModeBar": False},
                    ),
                    className="card",
                ),
                html.Br(),
                html.Div(
                    children=dcc.Graph(
                        id="quarter_graph",
                        config={"displayModeBar": False},
                    ),
                    className="card",
                ),
                html.Br()
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
        mask = (sales['data'] >= start_date) & (sales['data'] <= end_date)
        sales_filtered = sales.loc[mask]
        sales_per_year_filtered = (sales_filtered.groupby(sales_filtered.data.dt.year)['total'].sum()
                                   .reset_index()  # Rimozione multi index
                                   .rename(columns={'data': 'Anno', 'total': 'Totale'}))
        return px.bar(sales_per_year_filtered,
                      title="Fatturato",
                      x='Anno',
                      y='Totale',
                      text_auto=True).update_xaxes(type='category')


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
                      y='Totale',
                      text="Quarter")

