import psycopg2
import pandas as pd
from dash import html
from utils.db_connector import engine
pd.options.mode.chained_assignment = None  # default='warn'


def clean_df_for_articolo(df):
    try:
        articolo = df[['codice_art', 'descrizione_art', 'tipologia_art']]
        articolo = articolo.drop_duplicates(ignore_index=True)
        articolo = articolo.rename(
            columns={'codice_art': 'codice', 'descrizione_art': 'descrizione', 'tipologia_art': 'tipologia'})
        check = "SELECT codice, descrizione FROM articolo"
        keys = ['codice', 'descrizione']
        check_df = pd.read_sql(sql=check, con=engine)
        articolo = articolo.loc[
            articolo[keys].merge(check_df[keys], on=keys, how='left', indicator=True)['_merge'] == 'left_only']
        return articolo.dropna()
    except Exception as error:
        print(error, flush=True)


def clean_df_for_cliente(df):
    try:
        cliente = df[['codice_cli', 'ragione_sociale']]
        cliente = cliente.drop_duplicates(ignore_index=True)
        cliente = cliente.rename(
            columns={'codice_cli': 'codice_bms'})
        check = "SELECT codice_bms FROM cliente"
        keys = ['codice_bms']
        check_df = pd.read_sql(sql=check, con=engine)
        cliente = cliente.loc[
            cliente[keys].merge(check_df[keys], on=keys, how='left', indicator=True)['_merge'] == 'left_only']
        return cliente.dropna()
    except Exception as error:
        print(error, flush=True)


def clean_df_for_fattura(df):
    try:

        fattura = df[['nro_ftt', 'data_reg_ftt', 'codice_cli']]
        fattura = fattura.drop_duplicates(ignore_index=True)
        fattura = fattura[
            pd.to_numeric(fattura['nro_ftt'], errors='coerce').notnull()].reset_index(drop=True)
        print(fattura)
        fattura['nro_ftt'] = fattura['nro_ftt'].astype(int).apply(lambda x: str(x) + ' / F')
        fattura['data_reg_ftt'] = fattura['data_reg_ftt'].apply(lambda x: format_data(x))
        fattura = fattura.rename(
            columns={'nro_ftt': 'codice', 'data_reg_ftt': 'data', 'codice_cli': 'cliente_fk'})
        check = "SELECT codice, data FROM fattura"
        keys = ['codice', 'data']
        check_df = pd.read_sql(sql=check, con=engine)
        fattura = fattura.loc[
            fattura[keys].merge(check_df[keys], on=keys, how='left', indicator=True)['_merge'] == 'left_only']
        return fattura.dropna()
    except Exception as error:
        print(error, flush=True)


def clean_df_for_articolo_in_fattura(df):
    try:

        articolo_in_fattura = df[
            ['codice_art', 'nro_ftt', 'qta_venduta', 'data_reg_ftt', 'descrizione_art', 'prz_venduto']]
        articolo_in_fattura = articolo_in_fattura.drop_duplicates(ignore_index=True)

        #Check on numero fatture if is numeric
        articolo_in_fattura= articolo_in_fattura[
            pd.to_numeric(articolo_in_fattura['nro_ftt'], errors='coerce').notnull()].reset_index(drop=True)

        #Formatted numero fattura and data fattura
        articolo_in_fattura['nro_ftt'] = articolo_in_fattura['nro_ftt'].astype(int).apply(lambda x: str(x) + ' / F')
        articolo_in_fattura['data_reg_ftt'] = articolo_in_fattura['data_reg_ftt'].apply(lambda x: format_data(x))

        articolo_in_fattura = articolo_in_fattura.rename(
            columns={'codice_art': 'codice_articolo_fk',
                     'nro_ftt': 'codice_fattura_fk',
                     'qta_venduta': 'quantita',
                     'data_reg_ftt': 'data_fattura_fk',
                     'descrizione_art': 'descrizione_articolo_fk',
                     'prz_venduto': 'prezzo'})

        check = ("SELECT codice_articolo_fk, codice_fattura_fk, quantita, "
                 "data_fattura_fk, descrizione_articolo_fk, prezzo FROM articolo_in_fattura")

        keys = ['codice_articolo_fk', 'codice_fattura_fk', 'quantita',
                'data_fattura_fk', 'descrizione_articolo_fk', 'prezzo']

        check_df = pd.read_sql(sql=check, con=engine)
        articolo_in_fattura['prezzo'] = articolo_in_fattura['prezzo'].apply(lambda x: x.replace(',', '.'))
        articolo_in_fattura['prezzo'] = articolo_in_fattura['prezzo'].astype(float)
        articolo_in_fattura = articolo_in_fattura.loc[
            articolo_in_fattura[keys].merge(check_df[keys], on=keys, how='left', indicator=True)[
                '_merge'] == 'left_only']
        return articolo_in_fattura.dropna()
    except Exception as error:
        print(error, flush=True)


def format_data(data):
    try:
        data_splitted = data.split('/')
        year = data_splitted[2].split('00:00:00')
        formatted_data = year[0].strip() + '-' + data_splitted[1] + '-' + data_splitted[0]
        return formatted_data
    except Exception as error:
        print(error, flush=True)


def insert_data(df):
    string = ''

    # Articolo
    articolo = clean_df_for_articolo(df)
    try:
        res = articolo.to_sql(name='articolo', con=engine, schema='public', if_exists='append', index=False)
        string = string + ' Inseriti ' + str(res) + ' nuovi articoli'
    except psycopg2.errors.UniqueViolation as e:
        string = string + ' Inseriti 0 nuovi articoli\n'
    except Exception as e:
        string = string + ' Inseriti 0 nuovi articoli\n'
        print(e, flush=True)

    # Cliente
    cliente = clean_df_for_cliente(df)
    try:
        res = cliente.to_sql(name='cliente', con=engine, schema='public', if_exists='append', index=False)
        string = string + ' Inseriti ' + str(res) + ' nuovi clienti'
    except psycopg2.errors.UniqueViolation as e:
        string = string + ' Inseriti 0 nuovi clienti\n'
    except Exception as e:
        string = string + ' Inseriti 0 nuovi clienti\n'
        print(e, flush=True)

    # Fattura
    fattura = clean_df_for_fattura(df)
    try:
        res = fattura.to_sql(name='fattura', con=engine, schema='public', if_exists='append', index=False)
        string = string + ' Inserite ' + str(res) + ' nuove fatture'
    except psycopg2.errors.UniqueViolation as e:
        string = string + ' Inserite 0 nuove fatture'
    except Exception as e:
        string = string + ' Inserite 0 nuove fatture'
        print(e, flush=True)

    # Articolo in fattura
    articolo_in_fattura = clean_df_for_articolo_in_fattura(df)
    try:
        res = articolo_in_fattura.to_sql(name='articolo_in_fattura', con=engine, schema='public', if_exists='append',
                                         index=False)
        string = string + ' Inseriti ' + str(res) + ' nuovi articoli in fattura'
    except psycopg2.errors.UniqueViolation as e:
        string = string + ' Inseriti 0 nuovi articoli in fattura'
    except Exception as e:
        string = string + ' Inseriti 0 nuovi articoli in fattura'
        print(e, flush=True)

    return string


def insert_into_db(df):
    res = insert_data(df)
    return html.H5("Dati aggiornati correttamente - " + res)
