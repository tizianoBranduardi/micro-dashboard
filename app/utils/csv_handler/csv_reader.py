import pandas as pd
import psycopg2
from utils.db_connector import conn, engine
from dash import Dash, dcc, html, dash_table

def is_articolo_present(codice, descrizione):
    try:
        cursor = conn.cursor()
        select_query = "SELECT COUNT(*) FROM articolo WHERE codice = \'"+codice+"\' AND descrizione = \'"+descrizione+"\'"
        cursor.execute(select_query)
        count = cursor.fetchall()
        for row in count:
            print(row, flush=True)
            print(row[0] > 0, flush=True)
            cursor.close()
            return row[0] > 0

    except (Exception, psycopg2.Error) as error:
        print("Error while fetching data from PostgreSQL", error)


def insert_invoice(df):
    for index, row in df.iterrows():
        try:
            #Articolo
            print()
            if not is_articolo_present(row['codice_art'],row['descrizione_art']) :
                sql = "INSERT INTO articolo (codice, descrizione, tipologia) VALUES(%s,%s,%s)"
                cur = conn.cursor()
                print(row['codice_art'])
                cur.execute(sql, (row['codice_art'],row['descrizione_art'],row['tipologia_art']))
                print("Dati aggiornati correttamente", flush=True)
                conn.commit()
                cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        # insert_articolo = 'INSERT INTO TABLE articolo(codice, descrizione, tipologia) VALUES('+\
        #                 row['codice_art']+','+\
        #                 row['descrizione_art']+','+\
        #                 row['tipologia_art']
        

def insert_into_db(df):
    print("Test", flush=True)
    insert_invoice(df)
    return html.H5("Dati aggiornati correttamente")