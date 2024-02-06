import dash
import pandas as pd
import plotly.express as px
from dash import html, dcc, dash_table, callback, Output, Input
from utils.db_connector import engine, query_fatturato

pd.options.mode.chained_assignment = None  # default='warn'

dash.register_page(__name__)

colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}

sales = pd.read_sql(query_fatturato, engine)
sales['data'] = pd.to_datetime(sales['data'], format='%Y/%m/%d', utc=False)

dates = sales
dates['month'] = dates['data'].dt.month
dates['year'] = dates['data'].dt.year
dates = (dates[['month', 'year']]
         .drop_duplicates(ignore_index=True)
         .sort_values(by=['year', 'month'])
         .reset_index(drop=True))

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
        html.Br(),
        html.Div(
            children=[
                html.H4("Confronto percentuale"),
                html.P("Selezionare l'anno di riferimento"),
                html.Br(),
                dcc.Slider(
                    id='year_slider',
                    dots=True,
                    #value=dates['year'].min(),
                    min=dates['year'].min(),
                    max=dates['year'].max(),
                    step=1,
                    tooltip={"placement": "bottom", "always_visible": True},
                    marks=None
                ),
                html.Br(),
                html.Div(
                    children=dcc.Graph(
                        id="sales_graph_month",
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
    Output("sales_graph_month", "figure"),
    Input("year_slider", "value")
)
def update_sale_reference_graph(value):
    if not value:
        figure = px.line(sales_per_month,
                         title="Fatturato mensile - confronto percentuale",
                         #hover_name=sales_compared['Differenza'],
                         x='Mese',
                         y='Totale',
                         color='Anno',
                         markers=True).update_xaxes(type='category')
        return figure
    else:
        sales_compared = sales_per_month
        sales_compared['Differenza'] = ''
        sales_selected_year = sales_compared.loc[sales_compared['Anno'] == value]
        for index, row in sales_compared.iterrows():
            if (int(row['Mese']) in list(sales_selected_year['Mese'])) \
                    & (int(row['Anno']) != value):
                reference_value = \
                    sales_selected_year.loc[sales_selected_year['Mese'] == int(row['Mese'])]['Totale'].iloc[0]
                percentage = (row['Totale'] / reference_value) - 1
                percentage = " {:.2%}".format(percentage) if percentage < 0 else " +{:.2%}".format(percentage)
                sales_compared.loc[index, 'Differenza'] = "{} rispetto a {}".format(percentage, value)
        sales_compared.sort_values(by=['Mese', 'Anno'], inplace=True)
        figure = px.line(sales_compared,
                         title="Fatturato mensile - confronto percentuale",
                         hover_name=sales_compared['Differenza'],
                         x='Mese',
                         y='Totale',
                         color='Anno',
                         markers=True).update_xaxes(type='category')
        for line in figure.data:

            if line.name != str(value):
                line.line.width = 1
            else:
                line.line.width = 4

        return figure
