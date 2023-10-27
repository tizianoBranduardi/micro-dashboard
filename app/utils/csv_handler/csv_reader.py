import pandas as pd
import psycopg2
from utils.db_connector import engine
from dash import Dash, dcc, html, dash_table


def clean_df_for_articolo(df):
    try:
        articolo = df[['codice_art', 'descrizione_art', 'tipologia_art']]
        articolo = articolo.rename(
            columns={'codice_art': 'codice', 'descrizione_art': 'descrizione', 'tipologia_art': 'tipologia'})
        check = "SELECT codice, descrizione, tipologia FROM articolo"
        keys = ['codice', 'descrizione', 'tipologia']
        check_df = pd.read_sql(sql=check, con=engine)
        articolo = articolo.loc[articolo[keys].merge(check_df[keys], on=keys, how='left', indicator=True)['_merge'] == 'left_only']
        return articolo
    except Exception as error:
        print(error, flush=True)


def is_cliente_present(codice_bms):
    try:
        cursor = conn.cursor()
        select_query = "SELECT COUNT(*) FROM cliente WHERE codice_bms = " + str(codice_bms)
        cursor.execute(select_query)
        count = cursor.fetchall()
        for row in count:
            cursor.close()
            return row[0] > 0

    except (Exception, psycopg2.Error) as error:
        conn.rollback()
        print(error, flush=True)
        return True


def is_fattura_present(codice, data):
    try:
        cursor = conn.cursor()
        select_query = "SELECT COUNT(*) FROM fattura WHERE codice = \'" + str(codice) + "\' AND data = \'" + str(
            data) + "\'"
        cursor.execute(select_query)
        count = cursor.fetchall()
        for row in count:
            return row[0] > 0

    except (Exception, psycopg2.Error) as error:
        conn.rollback()
        print(error, flush=True)


def is_articolo_in_fattura_present(codice_articolo, codice_fattura, quantita, data_fattura, descrizione_articolo,
                                   prezzo):
    try:
        cursor = conn.cursor()
        select_query = "SELECT COUNT(*) FROM fattura\
                         WHERE codice_articolo_fk = \'" + codice_articolo + "\' AND codice_fattura_fk = \'" + codice_fattura + "\'\
                         AND quantita = \'" + quantita + "\' AND data_fattura_fk = \'" + data_fattura + "\'\
                         AND descrizione_articolo_fk = \'" + descrizione_articolo + "\' AND prezzo = \'" + prezzo + "\'"
        cursor.execute(select_query)
        count = cursor.fetchall()
        for row in count:
            cursor.close()
            return row[0] > 0

    except (Exception, psycopg2.Error) as error:
        conn.rollback()
        print(error, flush=True)


def format_data(data):
    data_splitted = data.split('/')
    year = data_splitted[2].split('00:00:00')
    formatted_data = year[0].strip() + '-' + data_splitted[1] + '-' + data_splitted[0]
    return formatted_data


def insert_data(df):
    string = ''
    articolo = clean_df_for_articolo(df)
    try:
        res = articolo.to_sql(name='articolo', con=engine, schema='public', if_exists='append', index=False)
        string = string + ' Inseriti '+str(res)+' nuovi articoli'
    except Exception as e:
        print(e, flush=True)



    return string

    # for index, row in df.iterrows():
    #     try:
    #         # Articolo
    #         if not is_articolo_present(row['codice_art'], row['descrizione_art']):
    #             print("Inserting articolo", flush=True)
    #             sql = "INSERT INTO articolo (codice, descrizione, tipologia) VALUES(%s,%s,%s)"
    #             cur = conn.cursor()
    #             cur.execute(sql, (row['codice_art'], row['descrizione_art'], row['tipologia_art']))
    #             print("Articolo aggiornato correttamente", flush=True)
    #             conn.commit()
    #             cur.close()
    #         # Cliente
    #         if not is_cliente_present(row['codice_cli']):
    #             print("Inserting cliente", flush=True)
    #             sql = "INSERT INTO cliente (codice_bms, ragione_sociale) VALUES(%s,%s)"
    #             cur = conn.cursor()
    #             cur.execute(sql, (row['codice_cli'], row['ragione_sociale']))
    #             print("Cliente aggiornato correttamente", flush=True)
    #             conn.commit()
    #             cur.close()
    #         # Fattura
    #         if not is_fattura_present(row['nro_ftt'], format_data(row['data_reg_ftt'])):
    #             print("Inserting fattura", flush=True)
    #             sql = "INSERT INTO fattura (codice, data, cliente_fk) VALUES(%s,%s)"
    #             cur = conn.cursor()
    #             cur.execute(sql, (row['nro_ftt'], format_data(row['data_reg_ftt']), row['codice_bms']))
    #             print("Fattura aggiornata correttamente", flush=True)
    #             conn.commit()
    #             cur.close()
    #         # Articolo in fattura
    #         if not is_articolo_in_fattura_present(row['codice_art'], row['nro_ftt'], row['qta_venduta'],
    #                                               format_data(row['data_reg_ftt']), row['descrizione_art'],
    #                                               row['prz_venduto']):
    #             print("Inserting articolo in fattura", flush=True)
    #             sql = "INSERT INTO articolo_in_fattura (codice_articolo_fk, codice_fattura_fk, quantita, \
    #                     data_fattura_fk, descrizione_articolo_fk, prezzo) VALUES(%s,%s,%s,%s,%s,%s)"
    #             cur = conn.cursor()
    #             cur.execute(sql, (row['codice_art'], row['nro_ftt'], row['qta_venduta'],
    #                               format_data(row['data_reg_ftt']), row['descrizione_art'], row['prz_venduto']))
    #             print("Articolo in fattura aggiornato correttamente", flush=True)
    #             conn.commit()
    #             cur.close()
    #
    #     except (Exception, psycopg2.DatabaseError) as error:
    #         print(error)


def insert_into_db(df):
    res = insert_data(df)
    return html.H5("Dati aggiornati correttamente - " + res)
