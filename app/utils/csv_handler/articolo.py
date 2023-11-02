import psycopg2
import pandas as pd
from utils.db_connector import engine
pd.options.mode.chained_assignment = None  # default='warn'

csv_columns = ['codice_art', 'descrizione_art', 'tipologia_art']
db_attributes_map = {'codice_art': 'codice', 'descrizione_art': 'descrizione', 'tipologia_art': 'tipologia'}
check_query = "SELECT codice, descrizione FROM articolo"
def clean_df_for_articolo(df):
    try:
        articolo = df[csv_columns]

        articolo = articolo.drop_duplicates(ignore_index=True)
        articolo = articolo.rename(columns=db_attributes_map)
        # check = check_query
        # keys = ['codice', 'descrizione']
        # check_df = pd.read_sql(sql=check, con=engine)
        # articolo = articolo.loc[
        #     articolo[keys].merge(check_df[keys], on=keys, how='left', indicator=True)['_merge'] == 'left_only']
        return articolo.dropna()
    except Exception as error:
        print(error, flush=True)

def insert_articolo(articolo):
    try:
        #res = insert_or_ignore(articolo, 'articolo', ['codice', 'descrizione'], ['codice', 'descrizione', 'tipologia'])
        res = articolo.to_sql(name='articolo', con=engine, schema='public', if_exists='append', index=False)
        return 'Inseriti ' + str(res) + ' nuovi articoli'
    except psycopg2.errors.UniqueViolation as e:
        return 'Inseriti 0 nuovi articoli'
    except Exception as e:
        #print(e, flush=True)
        return 'Inseriti 0 nuovi articoli'