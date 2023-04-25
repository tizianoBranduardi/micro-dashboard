import os
from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd
import psycopg2

conn = psycopg2.connect(
    host="micro-dashboard_db_1",
    database="micro_dashboard",
    user="postgres",
    password="postgres")

debug = False if os.environ["DASH_DEBUG_MODE"] == "False" else True

app = Dash(__name__)

server = app.server

# data = pd.DataFrame(
#     {
#         "Fruit": ["Apples", "Oranges", "Bananas", "Apples", "Oranges", "Bananas"],
#         "Amount": [4, 1, 2, 2, 4, 5],
#         "City": ["SF", "SF", "SF", "Montreal", "Montreal", "Montreal"],
#     }
# )
data = pd.read_sql('SELECT * FROM articolo LIMIT 5', conn)
print(data)


#graph = px.bar(data, x="Fruit", y="Amount", color="City", barmode="group")

app.layout = html.Div(
    children=[
        html.H1(
            children=f"Hello Dash from {'Dev Server' if debug else 'Prod Server'}"
        ),
        html.Div(children="""Dash: A web application framework for your data."""),
        html.Div(data.to_html()),
        #dcc.Graph(id="example-graph", figure=graph),
    ]
)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="8050", debug=debug)
