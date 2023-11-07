import psycopg2
import pandas as pd
from utils.db_connector import engine

pd.options.mode.chained_assignment = None  # default='warn'

csv_columns = ['CARTI', 'TARTI']
db_attributes_map = {'CARTI': 'codice', 'TARTI': 'descrizione'}


def clean_df_for_articolo(df):
    try:
        articolo = df[csv_columns]

        articolo = articolo.drop_duplicates(ignore_index=True)
        articolo = articolo.rename(columns=db_attributes_map)

        return articolo.dropna()
    except Exception as error:
        print(error, flush=True)


def insert_articolo(articolo):
    try:
        res = articolo.to_sql(name='articolo', con=engine, schema='public', if_exists='append', index=False)
        return 'Inseriti ' + str(res) + ' nuovi articoli'
    except Exception as e:
        # print(e, flush=True)
        return 'Nessun articolo inserito'
