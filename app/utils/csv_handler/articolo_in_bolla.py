import psycopg2
import pandas as pd
from utils.db_connector import engine
from utils.csv_handler.parse_number import *

pd.options.mode.chained_assignment = None  # default='warn'

csv_columns = ['CARTI', 'TARTI', 'CCAUS_SDOCU', 'CTIPO_DRIGD', 'NPROT_DDOCU', 'CUNMI_DMAGA', 'QMOMA', 'APREZ']
db_attributes_map = {'CARTI': 'codice_articolo_fk', 'TARTI': 'descrizione_articolo_fk',
                     'CCAUS_SDOCU': 'causale_bolla_fk', 'CTIPO_DRIGD': 'tipo_bolla_fk',
                     'NPROT_DDOCU': 'numero_bolla_fk',
                     'CUNMI_DMAGA': 'unita_misura', 'QMOMA': 'numero_unita', 'APREZ': 'prezzo_unitario'}


def clean_df_for_articolo_in_bolla(df):
    try:

        articolo_in_bolla = df[csv_columns]
        articolo_in_bolla = articolo_in_bolla.drop_duplicates(ignore_index=True)
        articolo_in_bolla = articolo_in_bolla.rename(columns=db_attributes_map)

        articolo_in_bolla['prezzo_unitario'] = articolo_in_bolla['prezzo_unitario'].apply(lambda x: parseNumber(x))

        return articolo_in_bolla.dropna()
    except Exception as error:
        print(error, flush=True)


def insert_articolo_in_bolla(articolo_in_bolla):
    try:
        res = articolo_in_bolla.to_sql(name='articolo_in_bolla', con=engine, schema='public', if_exists='append', index=False)
        return 'Inseriti ' + str(res) + ' nuovi articoli in bolla'
    except Exception as e:
        # print(e, flush=True)
        return 'Nessun articolo in bolla inserito'
