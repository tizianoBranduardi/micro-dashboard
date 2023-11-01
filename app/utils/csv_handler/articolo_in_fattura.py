import psycopg2
import pandas as pd
from utils.db_connector import engine
from utils.csv_handler.date_format import format_date
from utils.csv_handler.update_handler import *

pd.options.mode.chained_assignment = None  # default='warn'

csv_columns = ['codice_art', 'nro_ftt', 'qta_venduta', 'data_reg_ftt', 'descrizione_art', 'prz_venduto']
db_attributes_map = {'codice_art': 'codice_articolo_fk',
                     'nro_ftt': 'codice_fattura_fk',
                     'qta_venduta': 'quantita',
                     'data_reg_ftt': 'data_fattura_fk',
                     'descrizione_art': 'descrizione_articolo_fk',
                     'prz_venduto': 'prezzo'}
check_query = ("SELECT codice_articolo_fk, codice_fattura_fk,quantita,data_fattura_fk,descrizione_articolo_fk,prezzo "
               "FROM articolo_in_fattura")


def clean_df_for_articolo_in_fattura(df):
    try:

        articolo_in_fattura = df[csv_columns]
        articolo_in_fattura = articolo_in_fattura.rename(
            columns=db_attributes_map)
        articolo_in_fattura = articolo_in_fattura.drop_duplicates(ignore_index=True)

        # Check on numero fatture if is numeric
        articolo_in_fattura = articolo_in_fattura[
            pd.to_numeric(articolo_in_fattura['codice_fattura_fk'], errors='coerce').notnull()].reset_index(drop=True)

        # Formatted numero fattura and data fattura
        articolo_in_fattura['codice_fattura_fk'] = articolo_in_fattura['codice_fattura_fk'].astype(int).apply(
            lambda x: str(x) + ' / F')
        articolo_in_fattura['data_fattura_fk'] = articolo_in_fattura['data_fattura_fk'].apply(lambda x: format_date(x))
        articolo_in_fattura['data_fattura_fk'] = pd.to_datetime(articolo_in_fattura['data_fattura_fk'])
        articolo_in_fattura['prezzo'] = articolo_in_fattura['prezzo'].apply(lambda x: x.replace(',', '.'))
        articolo_in_fattura['prezzo'] = articolo_in_fattura['prezzo'].astype(float)

        # check = (check_query)
        # keys = ['codice_articolo_fk', 'codice_fattura_fk', 'quantita',
        #         'data_fattura_fk', 'descrizione_articolo_fk', 'prezzo']
        # check_df = pd.read_sql(sql=check, con=engine)
        # articolo_in_fattura = articolo_in_fattura.loc[
        #     articolo_in_fattura[keys].merge(check_df[keys], on=keys, how='left', indicator=True)[
        #         '_merge'] == 'left_only']
        return articolo_in_fattura.dropna()
    except Exception as error:
        print(error, flush=True)


def insert_articolo_in_fattura(articolo_in_fattura):
    try:
        # res = insert_or_ignore(articolo_in_fattura, 'articolo_in_fattura',
        #                        keys=['codice_articolo_fk', 'codice_fattura_fk', 'quantita', 'data_fattura_fk',
        #                         'descrizione_articolo_fk', 'prezzo'],
        #                        fields=['codice_articolo_fk', 'codice_fattura_fk', 'quantita', 'data_fattura_fk',
        #                         'descrizione_articolo_fk', 'prezzo'])
        res = articolo_in_fattura.to_sql(name='articolo_in_fattura', con=engine, schema='public', if_exists='append',
                                         index=False)
        return 'Inseriti ' + str(res) + ' nuovi articoli in fattura'
    except psycopg2.errors.UniqueViolation as e:
        return 'Inseriti 0 nuovi articoli in fattura'
    except Exception as e:
        #print(e, flush=True)
        return 'Inseriti 0 nuovi articoli in fattura'
