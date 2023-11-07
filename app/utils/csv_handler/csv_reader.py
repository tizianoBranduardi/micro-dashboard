import psycopg2
import pandas as pd
from dash import html
from utils.csv_handler.articolo import *
from utils.csv_handler.cliente import *
from utils.csv_handler.bolla import *
from utils.csv_handler.articolo_in_bolla import *


# from utils.csv_handler.fattura import *
# from utils.csv_handler.articolo_in_fattura import *

pd.options.mode.chained_assignment = None  # default='warn'


def insert_data(df):
    string = ''

    #Articolo
    articolo = clean_df_for_articolo(df)
    articolo_inserted = insert_articolo(articolo)
    print(articolo_inserted)

    # Cliente
    cliente = clean_df_for_cliente(df)
    cliente_inserted = insert_cliente(cliente)
    print(cliente_inserted)

    # Bolla
    bolla = clean_df_for_bolla(df)
    bolla_inserted = insert_bolla(bolla)
    print(bolla_inserted)

    #Articolo in bolla
    articolo_in_bolla = clean_df_for_articolo_in_bolla(df)
    articolo_in_bolla_inserted = insert_articolo_in_bolla(articolo_in_bolla)
    print(articolo_in_bolla_inserted)

    # # Fattura
    # fattura = clean_df_for_fattura(df)
    # fattura_inserted = insert_fattura(fattura)
    # print(fattura_inserted)

    # # Articolo in fattura
    # articolo_in_fattura = clean_df_for_articolo_in_fattura(df)
    # articolo_in_fattura_inserted = insert_articolo_in_fattura(articolo_in_fattura)
    # print(articolo_in_fattura_inserted)

    return string


def insert_into_db(df):
    res = ''
    df.rename(columns=lambda x: x.strip(), inplace=True)
    columns_list = df.columns.tolist()
    for row in df.values:
        row_df = pd.DataFrame(columns=columns_list, index=[0])
        row_df.loc[0] = row
        insert_data(row_df)

    return html.H5("Dati aggiornati correttamente")
