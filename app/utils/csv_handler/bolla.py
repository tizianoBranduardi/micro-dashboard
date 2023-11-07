import psycopg2
import pandas as pd
from utils.db_connector import engine
from utils.csv_handler.date_format import format_date
pd.options.mode.chained_assignment = None  # default='warn'

csv_columns = ['CCAUS_SDOCU', 'CTIPO_DRIGD', 'NPROT_DDOCU', 'DDOCU', 'NCOCG.1', 'TMPAG', 'TPORT', 'TRASO']
db_attributes_map = {'CCAUS_SDOCU': 'causale', 'CTIPO_DRIGD': 'tipo', 'NPROT_DDOCU': 'numero', 'DDOCU': 'data',
                     'NCOCG.1': 'cliente_fk', 'TMPAG': 'pagamento', 'TPORT': 'trasporto', 'TRASO': 'vettore'}
def clean_df_for_bolla(df):
    try:
        bolla = df[csv_columns]

        bolla = bolla.drop_duplicates(ignore_index=True)
        bolla = bolla.rename(columns=db_attributes_map)
        bolla['data'] = bolla['data'].apply(lambda x: format_date(x))
        bolla['data'] = pd.to_datetime(bolla['data'])
        return bolla.dropna()
    except Exception as error:
        print(error, flush=True)

def insert_bolla(bolla):
    try:
        res = bolla.to_sql(name='bolla', con=engine, schema='public', if_exists='append', index=False)
        return 'Inserite ' + str(res) + ' nuove bolle'
    except Exception as e:
        print(e, flush=True)
        return 'Nessuna bolla inserita'