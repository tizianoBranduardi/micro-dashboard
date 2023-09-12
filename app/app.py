import os
from dash import Dash, html, dcc, dash_table
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

query_homepage = 'SELECT F.codice, F.data, C.ragione_sociale, A.codice, A.descrizione, A_F.quantita, A_F.prezzo\
                FROM fattura AS F\
                JOIN articolo_in_fattura AS A_F ON F.data = A_F.data_fattura_fk AND F.codice = A_F.codice_fattura_fk\
                JOIN articolo AS A ON A.codice = A_F.codice_articolo_fk AND A.descrizione = A_F.descrizione_articolo_fk\
                JOIN cliente AS C ON F.cliente_fk = C.codice_bms'

data = pd.read_sql(query_homepage, conn)

app.layout = html.Div(
    children=[
        html.H1(
            children=f"Hello Dash from {'Dev Server' if debug else 'Prod Server'}"
        ),
        html.Div(children="""Dash: A web application framework for your data."""),
        dash_table.DataTable(data.to_dict('records'),
                            [{"name": i, "id": i} for i in data.columns],
                            sort_action="native",
                            sort_mode='multi',
                            filter_action="native",
                            filter_options={"placeholder_text": "Filter column..."},
                            page_size=10,),
    ]
)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port="8050", debug=debug, threaded=True)
