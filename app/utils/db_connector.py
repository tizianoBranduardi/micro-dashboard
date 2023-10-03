import psycopg2
from sqlalchemy import create_engine

conn = psycopg2.connect(
    host="micro-dashboard_db_1",
    database="micro_dashboard",
    user="postgres",
    password="postgres")

engine = create_engine('postgresql+psycopg2://postgres:postgres@micro-dashboard_db_1/micro_dashboard')

query_homepage = 'SELECT F.codice, F.data, C.ragione_sociale, A.codice, A.descrizione, A_F.quantita, A_F.prezzo\
                FROM fattura AS F\
                JOIN articolo_in_fattura AS A_F ON F.data = A_F.data_fattura_fk AND F.codice = A_F.codice_fattura_fk\
                JOIN articolo AS A ON A.codice = A_F.codice_articolo_fk AND A.descrizione = A_F.descrizione_articolo_fk\
                JOIN cliente AS C ON F.cliente_fk = C.codice_bms'