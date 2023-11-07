import psycopg2
import pandas as pd
from utils.db_connector import engine
pd.options.mode.chained_assignment = None  # default='warn'

csv_columns = ['NCOCG.1', 'TRASO.1', 'AGENTE']
db_attributes_map = {'NCOCG.1': 'codice_bms', 'TRASO.1': 'ragione_sociale', 'AGENTE': 'commerciale'}

def clean_df_for_cliente(df):
    try:
        cliente = df[csv_columns]
        cliente = cliente.drop_duplicates(ignore_index=True)
        cliente = cliente.rename(columns=db_attributes_map)

        return cliente.dropna()
    except Exception as error:
        print(error, flush=True)

def insert_cliente(cliente):
    try:
        res = cliente.to_sql(name='cliente', con=engine, schema='public', if_exists='append', index=False)
        return 'Inseriti ' + str(res) + ' nuovi clienti'
    except Exception as e:
        #print(e, flush=True)
        return 'Nessun cliente inserito'

