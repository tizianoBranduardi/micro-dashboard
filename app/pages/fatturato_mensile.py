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

dates = sales["data"].sort_values().unique()

sales_mod = sales[['data', 'total']]
sales_mod['day'] = sales_mod['data'].dt.day
sales_mod['month'] = sales_mod['data'].dt.month
sales_mod['year'] = sales_mod['data'].dt.year
sales_mod.set_index('year', inplace=True)
sales_mod.sort_values(by=['year', 'month'], inplace=True)

sales_per_month = (sales_mod.groupby(['month', 'year'])['total'].sum()
                   .reset_index()
                   .rename(columns={'year': 'Anno', 'month': 'Mese', 'total': 'Totale'}))

monthly_sales_graph = px.line(sales_per_month,
                              title="Fatturato mensile",
                              x='Mese',
                              y='Totale',
                              color='Anno',
                              markers=True).update_xaxes(type='category')

sales_cumsum = (sales_per_month
                .join(sales_per_month.groupby(['Anno'], as_index=False)['Totale'].cumsum(), rsuffix="_cumsum")
                .reset_index()
                .rename(columns={'Totale_cumsum': 'Fatturato Cumulato'}))

sales_cumsum.sort_values(by=['Mese', 'Anno'], inplace=True)

monthly_sales_cumsum_graph = px.line(sales_cumsum,
                                     title="Fatturato mensile cumulato",
                                     x='Mese',
                                     y='Fatturato Cumulato',
                                     color='Anno',
                                     markers=True).update_xaxes(type='category')

layout = html.Div(
    children=[
        html.Br(),
        html.H4(
            children="Analisi Fatturato - Scope mese"
        ),
        # html.Div(
        #     children=[
        #         html.Div(
        #             children="Mesi"  # , className="menu-title"
        #         ),
        #         html.Br(),
        #         dcc.DatePickerRange(
        #             id="date-range",
        #             min_date_allowed=sales["data"].min(),
        #             max_date_allowed=sales["data"].max(),
        #             start_date=sales["data"].min(),
        #             end_date=sales["data"].max(),
        #         ),
        #     ]
        # ),
        html.Br(),
        html.Div(
            children=[
                html.Div(
                    children=dcc.Graph(
                        id="sales_graph_month",
                        figure=monthly_sales_graph,
                        config={"displayModeBar": False},
                    ),
                    className="card",
                ),
                html.Br(),
                html.Div(
                    children=dcc.Graph(
                        id="sales_graph_month",
                        figure=monthly_sales_cumsum_graph,
                        config={"displayModeBar": False},
                    ),
                    className="card",
                ),
            ],
            className="wrapper",
        ),
    ]
)

# @callback(
#     Output("sales_graph_month", "figure"),
#     [Input("date-range", "start_date"),
#      Input("date-range", "end_date")]
# )
# def update_sale_graph(start_date, end_date):
#     if not start_date or not end_date:
#         raise dash.exceptions.PreventUpdate
#     else:
#         mask = (sales['data'] >= start_date) & (sales['data'] <= end_date)
#         sales_filtered = sales.loc[mask]
#         sales_filtered = sales_filtered[['data', 'total']]
#         sales_filtered['day'] = sales_filtered['data'].dt.day
#         sales_filtered['month'] = sales_filtered['data'].dt.month
#         sales_filtered['year'] = sales_filtered['data'].dt.year
#         sales_per_month_filtered = (sales_filtered.groupby(['year', 'month'])['total'].sum()
#                                     .reset_index()
#                                     .rename(columns={'year': 'Anno', 'month': 'Mese', 'total': 'Totale'}))
#
#         return px.line(sales_per_month_filtered,
#                        title="Fatturato",
#                        x='Mese',
#                        y='Totale',
#                        color='Anno').update_xaxes(type='category')
