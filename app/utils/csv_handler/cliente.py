import psycopg2
import pandas as pd
from utils.db_connector import engine
from utils.csv_handler.update_handler import *
pd.options.mode.chained_assignment = None  # default='warn'

csv_columns = ['codice_cli', 'ragione_sociale']
db_attributes_map = {'codice_cli': 'codice_bms'}
check_query = "SELECT codice_bms FROM cliente"

def clean_df_for_cliente(df):
    try:
        cliente = df[csv_columns]
        cliente = cliente.drop_duplicates(ignore_index=True)
        cliente = cliente.rename(columns=db_attributes_map)
        # check = check_query
        # keys = ['codice_bms']
        # check_df = pd.read_sql(sql=check, con=engine)
        # cliente = cliente.loc[
        #     cliente[keys].merge(check_df[keys], on=keys, how='left', indicator=True)['_merge'] == 'left_only']
        return cliente.dropna()
    except Exception as error:
        print(error, flush=True)

def insert_cliente(cliente):
    try:
        #res = insert_or_ignore(cliente, 'cliente', ['codice_bms'], ['codice_bms', 'ragione_sociale'])
        res = cliente.to_sql(name='cliente', con=engine, schema='public', if_exists='append', index=False)
        return 'Inseriti ' + str(res) + ' nuovi clienti'
    except psycopg2.errors.UniqueViolation as e:
        return 'Inseriti 0 nuovi clienti'
    except Exception as e:
        #print(e, flush=True)
        return 'Inseriti 0 nuovi clienti'

